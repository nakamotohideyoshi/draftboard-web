import * as ReactRedux from 'react-redux';
import isEqual from 'lodash/isEqual';
import log from '../../lib/logging';
import Pusher from '../../lib/pusher';
import React from 'react';
import { bindActionCreators } from 'redux';
import { lineupsHaveRelatedInfoSelector } from '../../selectors/current-lineups';
import { onBoxscoreGameReceived, onBoxscoreTeamReceived } from '../../actions/events/boxscores';
import { onPBPReceived, onPBPEventReceived } from '../../actions/events/pbp';
import { onPlayerStatsReceived } from '../../actions/events/stats';
import {
  relevantGamesPlayersSelector, watchingDraftGroupTimingSelector,
} from '../../selectors/watching';

// get custom logger for actions
const logComponent = log.getLogger('component');


/*
 * Map Redux actions to React component properties
 * @param  {function} dispatch The dispatch method to pass actions into
 * @return {object}            All of the methods to map to the component, wrapped in 'action' key
 */
const mapDispatchToProps = (dispatch) => ({
  actions: bindActionCreators({
    onBoxscoreGameReceived,
    onBoxscoreTeamReceived,
    onPBPReceived,
    onPBPEventReceived,
    onPlayerStatsReceived,
  }, dispatch),
});

/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
const mapStateToProps = (state) => ({
  draftGroupTiming: watchingDraftGroupTimingSelector(state),
  hasRelatedInfo: lineupsHaveRelatedInfoSelector(state),
  relevantGamesPlayers: relevantGamesPlayersSelector(state),
  watching: state.watching,
});

/*
 * The overarching component for handling pusher data
 */
export const PusherData = React.createClass({

  propTypes: {
    actions: React.PropTypes.object.isRequired,
    draftGroupTiming: React.PropTypes.object.isRequired,
    hasRelatedInfo: React.PropTypes.bool.isRequired,
    params: React.PropTypes.object,
    relevantGamesPlayers: React.PropTypes.object.isRequired,
    watching: React.PropTypes.object.isRequired,
  },

  getInitialState() {
    // NOTE: this really bogs down your console, only use locally when needed
    // uncomment this ONLY if you need to debug why Pusher isn't connecting
    // Pusher.log = (message) => logComponent.trace('pusher', message);

    return {
      // prefix allows us to silo data when developing, is based on the [PUSHER_CHANNEL_PREFIX] django const
      channelPrefix: window.dfs.user.pusher_channel_prefix.toString(),
      // loaded booleans used to prevent repeat pusher bindings
      loadedBoxscores: false,
      loadedForSport: false,
      // pusher is a singleton, keep it accessible within the component
      pusher: Pusher,
    };
  },

  /**
   * Receive socket messages when everything is ready
   */
  componentWillReceiveProps(nextProps) {
    if (nextProps.hasRelatedInfo &&
        nextProps.draftGroupTiming.started
    ) {
      if (!this.state.loadedBoxscores) {
        const boxscoresChannel = this.state.pusher.subscribe(`${this.state.channelPrefix}boxscores`);
        boxscoresChannel.bind('game', (message) => this.props.actions.onBoxscoreGameReceived(message));
        boxscoresChannel.bind('team', (message) => this.props.actions.onBoxscoreTeamReceived(message));

        this.setState({ loadedBoxscores: true });
      }

      // set sport specific sockets
      let oldSports = this.props.watching.sport || [];
      let newSports = nextProps.watching.sport || [];
      if (typeof oldSports === 'string') oldSports = [oldSports];
      if (typeof newSports === 'string') newSports = [newSports];

      // onload set sport
      if (!this.state.loadedForSport && newSports.length > 0) {
        this.subscribeToSportSockets(newSports);
      // switch sports
      } else if (isEqual(newSports.sort(), oldSports.sort()) === false) {
        this.unsubscribeToSportSockets(oldSports);
        this.subscribeToSportSockets(newSports);
      }
    }
  },

  /*
   * Start up Pusher listeners
   *
   * @param  {array} newSports  New sports to subscribe to
   */
  subscribeToSportSockets(newSports) {
    const { actions } = this.props;
    const { pusher, channelPrefix } = this.state;

    logComponent.debug('pusherData.subscribeToSockets', { channelPrefix, newSports });

    // note that when binding, we need to reference `this.props` so that when the event occurs, it pulls latest props
    newSports.map((sport) => {
      const pbpChannel = pusher.subscribe(`${channelPrefix}${sport}_pbp`);
      pbpChannel.bind('event', (message) => actions.onPBPEventReceived(message, sport));
      pbpChannel.bind('linked', (message) => actions.onPBPReceived(message, sport));

      const statsChannel = pusher.subscribe(`${channelPrefix}${sport}_stats`);
      statsChannel.bind('player', (message) => actions.onPlayerStatsReceived(
        message, sport, this.props.relevantGamesPlayers.relevantItems.games
      ));
    });

    this.setState({ loadedForSport: true });
  },

  /*
   * Shut down unneeded Pusher listeners
   *
   * @param  {array} oldSports  Old sports to unsubscribe from
   */
  unsubscribeToSportSockets(oldSports) {
    logComponent.debug('pusherData.unsubscribeToSockets');

    // if there's no old sports, don't bother
    if (oldSports.length === 0) return false;

    const { pusher, channelPrefix } = this.state;

    oldSports.map((sport) => {
      pusher.unsubscribe(`${channelPrefix}${sport}_pbp`);
      pusher.unsubscribe(`${channelPrefix}${sport}_stats`);
    });
  },

  render() {
    return null;
  },
});

// Set up Redux connection to React
const { connect } = ReactRedux;

// Wrap the component to inject dispatch and selected state into it.
export default connect(
  mapStateToProps,
  mapDispatchToProps
)(PusherData);
