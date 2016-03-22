import * as ReactRedux from 'react-redux';
import log from '../../lib/logging';
import Pusher from 'pusher-js';
import React from 'react';
import { addEventAndStartQueue } from '../../actions/pusher-live';
import { fetchSportIfNeeded } from '../../actions/sports';
import { intersection as _intersection } from 'lodash';
import { liveSelector } from '../../selectors/live';
import { map as _map } from 'lodash';
import { sportsSelector } from '../../selectors/sports';
import { updatePlayerStats } from '../../actions/live-draft-groups';


/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
const mapStateToProps = (state) => ({
  liveSelector: liveSelector(state),
  sportsSelector: sportsSelector(state),
});

/*
 * The overarching component for handling pusher data
 */
const PusherData = React.createClass({

  propTypes: {
    dispatch: React.PropTypes.func.isRequired,
    liveSelector: React.PropTypes.object.isRequired,
    params: React.PropTypes.object,
    sportsSelector: React.PropTypes.object.isRequired,
  },

  getInitialState() {
    return {
      channelPrefix: window.dfs.user.pusher_channel_prefix.toString(),
      pusher: new Pusher(window.dfs.user.pusher_key, {
        encrypted: true,
      }),
    };
  },

  /**
   * Uses promises in order to pull in all relevant data into redux, and then starts to listen for Pusher calls
   * Here's the documentation on the order in which all the data comes in https://goo.gl/uSCH0K
   */
  componentWillMount() {
    // always load up boxscores pusher
    const boxscoresChannel = this.state.pusher.subscribe(`${this.state.channelPrefix}boxscores`);
    boxscoresChannel.bind('team', this.onBoxscoreTeamReceived);
    boxscoresChannel.bind('game', this.onBoxscoreGameReceived);

    // NOTE: this really bogs down your console, only use locally when needed
    // uncomment this ONLY if you need to debug why Pusher isn't connecting
    Pusher.log = (message) => log.trace(message);
  },

  /**
   * If the sport has changed, update the socket subscriptions
   * @param  {[type]} prevProps [description]
   * @return {[type]}           [description]
   */
  componentDidUpdate(prevProps) {
    const oldSport = prevProps.liveSelector.mode.sport;
    const newSport = this.props.liveSelector.mode.sport;

    if (oldSport !== newSport) {
      this.unsubscribeToSportSockets(oldSport);
      this.subscribeToSportSockets(newSport);
    }
  },

  /*
   * Don't rerender the component every time the state, props update
   */
  // shouldComponentUpdate() {
  //   return false;
  // },

  /*
   * When we receive a Pusher stats call, make sure it's related to our games, and if so send to the appropriate queue
   *
   * @param  {object} eventCall The received event from Pusher
   */
  onBoxscoreGameReceived(eventCall) {
    log.trace('Live.onBoxscoreGameReceived()');
    const gameId = eventCall.id;

    // return if basic checks fail
    if (this.isPusherEventRelevant(eventCall, gameId) === false) {
      return;
    }

    // if the event didn't involve points, then don't bother bc that's all we deal with
    if (eventCall.hasOwnProperty('clock') === false) {
      log.debug('Live.onBoxscoreGameReceived() - call had no points', eventCall);
      return;
    }

    addEventAndStartQueue(eventCall.id, eventCall, 'boxscore-game');
  },

  /*
   * When we receive a Pusher stats call, make sure it's related to our games, and if so send to the appropriate queue
   *
   * @param  {object} eventCall The received event from Pusher
   */
  onBoxscoreTeamReceived(eventCall) {
    log.trace('Live.onBoxscoreTeamReceived()');
    const gameId = eventCall.game__id;

    // TODO Craig - remove this
    // current bug where player stats are being passed through in boxscore feed
    if (eventCall.model === `${this.props.liveSelector.mode.sport}.playerstats`) {
      this.onStatsReceived(eventCall);
      return;
    }

    // return if basic checks fail
    if (this.isPusherEventRelevant(eventCall, gameId) === false) {
      return;
    }

    // if the event didn't involve points, then don't bother bc that's all we deal with
    if (eventCall.hasOwnProperty('points') === false) {
      log.debug('Live.onBoxscoreTeamReceived() - call had no points', eventCall);
      return;
    }

    addEventAndStartQueue(eventCall.game__id, eventCall, 'boxscore-team');
  },

  /*
   * When we receive a Pusher stats call, make sure it's related to one the relevant players
   *
   * @param  {object} eventCall The received event from Pusher
   */
  onPBPReceived(eventCall) {
    log.trace('Live.onPBPReceived()');

    const isLinked = eventCall.hasOwnProperty('pbp');
    const eventData = isLinked ? eventCall.pbp : eventCall;
    const gameId = eventData.game__id;

    // return if basic checks fail
    if (this.isPusherEventRelevant(eventData, gameId) === false) {
      return;
    }

    // if this is not a statistical based call or has no location to animate, ignore
    if (eventData.hasOwnProperty('statistics__list') === false ||
        eventData.hasOwnProperty('location__list') === false
      ) {
      log.debug('Live.onPBPReceived() - had no statistics__list', eventCall);
      return;
    }

    const relevantPlayers = this.props.liveSelector.relevantPlayers;
    const eventPlayers = _map(eventData.statistics__list, event => event.player);

    // only add to the queue if we care about the player(s)
    if (_intersection(relevantPlayers, eventPlayers).length > 0) {
      addEventAndStartQueue(gameId, eventCall, 'pbp');
    }
  },

  /*
   * When we receive a Pusher stats call, make sure it's related to our games/players, and if so send to the appropriate
   * method to be parsed
   *
   * @param  {object} eventCall The received event from Pusher
   */
  onStatsReceived(eventCall) {
    log.trace('Live.onStatsReceived()');
    const gameId = eventCall.fields.srid_game;

    // return if basic checks fail
    if (this.isPusherEventRelevant(eventCall, gameId) === false) {
      return;
    }

    // if it's not a relevant game to the live section, then just update the player's FP to update the NavScoreboard
    if (this.props.liveSelector.relevantGames.indexOf(gameId) !== -1) {
      // otherwise just update the player's FP
      this.props.dispatch(updatePlayerStats(
        eventCall.fields.player_id,
        eventCall,
        this.props.liveSelector.lineups.mine.draftGroup.id
      ));
      return;
    }

    addEventAndStartQueue(gameId, eventCall, 'stats');
  },

  /*
   * Start up Pusher listeners to the necessary channels and events
   *
   * @param  {string} newSport New sport to subscribe to
   */
  subscribeToSportSockets(newSport) {
    log.trace('pusherData.subscribeToSockets()');

    // if there's no sport, then no need to subscribe
    if (newSport === null) {
      return;
    }

    const { pusher, channelPrefix } = this.state;

    const pbpChannel = pusher.subscribe(`${channelPrefix}${newSport}_pbp`);
    pbpChannel.bind('event', this.onPBPReceived);
    pbpChannel.bind('linked', this.onPBPReceived);

    const statsChannel = pusher.subscribe(`${channelPrefix}${newSport}_stats`);
    statsChannel.bind('player', this.onStatsReceived);
  },

  /*
   * Shut down Pusher listeners to the necessary channels and events
   *
   * @param  {string} oldSport Old sport to unsubscribe from
   */
  unsubscribeToSportSockets(oldSport) {
    log.trace('pusherData.unsubscribeToSockets()');

    // if there's no old sport, then no need to unsubscribe
    if (oldSport === null) {
      return;
    }

    const { pusher, channelPrefix } = this.state;
    pusher.unsubscribe(`${channelPrefix}${oldSport}_pbp`);
    pusher.unsubscribe(`${channelPrefix}${oldSport}_stats`);
  },

  /*
   * Check whether the Pusher call has the right information we need
   *
   * @return {Boolean} Whether the event is relevant to the live/nav sections
   */
  isPusherEventRelevant(eventCall, gameId) {
    // for now, only use calls once data is loaded
    if (this.props.liveSelector.hasRelatedInfo === false) {
      log.trace('Live.isPusherEventRelevant() - hasRelatedInfo === false', eventCall);
      return false;
    }

    if (this.props.liveSelector.draftGroupStarted === false) {
      log.trace('Live.isPusherEventRelevant() - in countdown mode', eventCall);
      return false;
    }

    const games = this.props.sportsSelector.games;

    // check that the game is relevant
    if (games.hasOwnProperty(gameId) === false) {
      log.trace('eventCall had irrelevant game', eventCall);
      return false;
    }

    // if we haven't received from the server that the game has started, then ask the server for an update!
    if (games[gameId].hasOwnProperty('boxscore') === false) {
      log.trace('Live.isPusherEventRelevant() - related game had no boxscore from server', eventCall);

      // by passing in a sport, you force
      this.props.dispatch(fetchSportIfNeeded(this.props.liveSelector.mode.sport, true));
      return false;
    }

    return true;
  },

  render() {
    return <div />;
  },
});

// Set up Redux connections to React
const { connect } = ReactRedux;

// Wrap the component to inject dispatch and selected state into it.
const PusherDataConnected = connect(
  mapStateToProps
)(PusherData);

export default PusherDataConnected;
