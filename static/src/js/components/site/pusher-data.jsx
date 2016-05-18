import * as ReactRedux from 'react-redux';
import log from '../../lib/logging';
import Pusher from 'pusher-js';
import React from 'react';
import { addEventAndStartQueue } from '../../actions/events';
import { fetchSportIfNeeded } from '../../actions/sports';
import { intersection as _intersection } from 'lodash';
import { watchingMyLineupSelector, relevantGamesPlayersSelector } from '../../selectors/watching';
import { forEach as _forEach } from 'lodash';
import { map as _map } from 'lodash';
import { merge as _merge } from 'lodash';
import { sportsSelector } from '../../selectors/sports';
import { updatePlayerStats } from '../../actions/live-draft-groups';
import { entriesHaveRelatedInfoSelector } from '../../selectors/entries';
import { watchingDraftGroupTimingSelector } from '../../selectors/watching';


/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
const mapStateToProps = (state) => ({
  draftGroupTiming: watchingDraftGroupTimingSelector(state),
  hasRelatedInfo: entriesHaveRelatedInfoSelector(state),
  relevantGamesPlayers: relevantGamesPlayersSelector(state),
  myLineup: watchingMyLineupSelector(state),
  watching: state.watching,
  sportsSelector: sportsSelector(state),
});

/*
 * The overarching component for handling pusher data
 */
const PusherData = React.createClass({

  propTypes: {
    dispatch: React.PropTypes.func.isRequired,
    draftGroupTiming: React.PropTypes.object.isRequired,
    hasRelatedInfo: React.PropTypes.bool.isRequired,
    relevantGamesPlayers: React.PropTypes.object.isRequired,
    myLineup: React.PropTypes.object.isRequired,
    watching: React.PropTypes.object.isRequired,
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
    let oldSports = prevProps.watching.sport || [];
    let newSports = this.props.watching.sport || [];

    // make sure we have an array TODO make sure it's this before we get to this point!
    if (typeof oldSports === 'string') oldSports = [oldSports];
    if (typeof newSports === 'string') newSports = [newSports];

    // if unchanged, then return
    if (oldSports.length > 0 && newSports.length > 0 && oldSports[0] === newSports[0]) return;

    this.unsubscribeToSportSockets(oldSports);
    this.subscribeToSportSockets(newSports);
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
    if (eventCall.hasOwnProperty('clock') === false && eventCall.hasOwnProperty('outcome__list') === false) {
      log.debug('Live.onBoxscoreGameReceived() - call had no time', eventCall);
      return;
    }

    // determine sports
    let sport = 'nba';
    if (eventCall.hasOwnProperty('outcome__list')) {
      sport = 'mlb';
    }

    addEventAndStartQueue(eventCall.id, eventCall, 'boxscore-game', sport);
  },

  /*
   * When we receive a Pusher stats call, make sure it's related to our games, and if so send to the appropriate queue
   *
   * @param  {object} eventCall The received event from Pusher
   */
  onBoxscoreTeamReceived(eventCall) {
    log.trace('Live.onBoxscoreTeamReceived()');
    const gameId = eventCall.game__id;

    // return if basic checks fail
    if (this.isPusherEventRelevant(eventCall, gameId) === false) {
      return;
    }

    // if the event didn't involve points, then don't bother bc that's all we deal with
    if (eventCall.hasOwnProperty('points') === false) {
      log.debug('Live.onBoxscoreTeamReceived() - call had no points', eventCall);
      return;
    }

    addEventAndStartQueue(eventCall.game__id, eventCall, 'boxscore-team', 'nba');
  },

  /*
   * When we receive a Pusher stats call, make sure it's related to one the relevant players
   *
   * @param  {object} eventCall The received event from Pusher
   */
  onPBPReceived(eventCall, sport) {
    log.trace('Live.onPBPReceived()');

    const isLinked = eventCall.hasOwnProperty('pbp');
    const eventData = isLinked ? eventCall.pbp : eventCall;
    const gameId = eventData.game__id;

    // return if basic checks fail
    if (this.isPusherEventRelevant(eventData, gameId) === false) {
      return;
    }

    let eventPlayers;
    const relevantPlayers = this.props.relevantGamesPlayers.relevantItems.players;

    switch (sport) {
      case 'mlb':
        eventPlayers = [
          eventData.pitcher,
        ];

        if (eventCall.hasOwnProperty('at_bat')) {
          eventPlayers.push(eventCall.at_bat.hitter_id);
        }
        break;
      case 'nba':
      default:
        // if this is not a statistical based call or has no location to animate, ignore
        if (eventData.hasOwnProperty('statistics__list') === false ||
            eventData.hasOwnProperty('location__list') === false
          ) {
          log.debug('Live.onPBPReceived() - had no statistics__list', eventCall);
          return;
        }

        eventPlayers = _map(eventData.statistics__list, event => event.player);
    }

    // make sure to add eventPlayers as its own entity on the call
    const eventWithExtraData = _merge(eventCall, {
      addedData: {
        eventPlayers,
        sport,
      },
    });

    // only add to the queue if we care about the player(s)
    if (_intersection(relevantPlayers, eventPlayers).length > 0) {
      addEventAndStartQueue(gameId, eventWithExtraData, 'pbp', sport);
    }
  },

  /*
   * When we receive a Pusher stats call, make sure it's related to our games/players, and if so send to the appropriate
   * method to be parsed
   *
   * @param  {object} eventCall The received event from Pusher
   * @param  {string} sport     The player's sport, used to parse in actions
   */
  onStatsReceived(eventCall, sport) {
    log.trace('Live.onStatsReceived()');
    const gameId = eventCall.fields.srid_game;

    // return if basic checks fail
    if (this.isPusherEventRelevant(eventCall, gameId) === false) {
      return;
    }

    if (this.props.relevantGamesPlayers.isLoading) return;

    // if it's not a relevant game to the live section, then just update the player's FP to update the NavScoreboard
    if (this.props.relevantGamesPlayers.relevantItems.games.indexOf(gameId) !== -1) {
      // otherwise just update the player's FP
      this.props.dispatch(updatePlayerStats(
        eventCall.fields.player_id,
        eventCall,
        this.props.myLineup.draftGroupId
      ));
      return;
    }

    addEventAndStartQueue(gameId, eventCall, 'stats', sport);
  },

  /*
   * Start up Pusher listeners to the necessary channels and events
   *
   * @param  {string} newSport New sport to subscribe to
   */
  subscribeToSportSockets(newSports) {
    log.trace('pusherData.subscribeToSockets()');

    // if there's no sport, then no need to subscribe
    if (newSports.length === 0) {
      return;
    }

    const { pusher, channelPrefix } = this.state;

    _forEach(newSports, (sport) => {
      const pbpChannel = pusher.subscribe(`${channelPrefix}${sport}_pbp`);
      pbpChannel.bind('event', (eventCall) => this.onPBPReceived(eventCall, sport));
      pbpChannel.bind('linked', (eventCall) => this.onPBPReceived(eventCall, sport));

      const statsChannel = pusher.subscribe(`${channelPrefix}${sport}_stats`);
      statsChannel.bind('player', (eventCall) => this.onStatsReceived(eventCall, sport));
    });
  },

  /*
   * Shut down Pusher listeners to the necessary channels and events
   *
   * @param  {string} oldSport Old sport to unsubscribe from
   */
  unsubscribeToSportSockets(oldSports) {
    log.trace('pusherData.unsubscribeToSockets()');

    // if there's no old sport, then no need to unsubscribe
    if (oldSports.length === 0) {
      return;
    }

    const { pusher, channelPrefix } = this.state;

    _forEach(oldSports, (sport) => {
      pusher.unsubscribe(`${channelPrefix}${sport}_pbp`);
      pusher.unsubscribe(`${channelPrefix}${sport}_stats`);
    });
  },

  /*
   * Check whether the Pusher call has the right information we need
   *
   * @return {Boolean} Whether the event is relevant to the live/nav sections
   */
  isPusherEventRelevant(eventCall, gameId) {
    // for now, only use calls once data is loaded
    if (this.props.hasRelatedInfo === false) {
      log.trace('Live.isPusherEventRelevant() - hasRelatedInfo === false', eventCall);
      return false;
    }

    if (this.props.draftGroupTiming.started === false) {
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
      this.props.dispatch(fetchSportIfNeeded(this.props.watching.sport, true));
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
