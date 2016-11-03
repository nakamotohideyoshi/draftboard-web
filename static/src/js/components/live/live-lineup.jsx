import * as ReactRedux from 'react-redux';
import LiveLineupPlayer from './live-lineup-player';
import React from 'react';
import { bindActionCreators } from 'redux';
import { fetchSinglePlayerBoxScoreHistoryIfNeeded } from '../../actions/player-box-score-history-actions';
import { updateLiveMode, updateWatchingAndPath } from '../../actions/watching';
import {
  relevantPlayerBoxScoreHistoriesSelector,
  relevantPlayerTeamsSelector,
  relevantPlayersSelector,
} from '../../selectors/live-players';

// assets
require('../../../sass/blocks/live/live-lineup.scss');


/*
 * Map Redux actions to React component properties
 * @param  {function} dispatch The dispatch method to pass actions into
 * @return {object}            All of the methods to map to the component, wrapped in 'action' key
 */
const mapDispatchToProps = (dispatch) => ({
  actions: bindActionCreators({
    fetchSinglePlayerBoxScoreHistoryIfNeeded,
    updateLiveMode,
    updateWatchingAndPath,
  }, dispatch),
});

/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
const mapStateToProps = (state) => ({
  playerEventDescriptions: state.events.playerEventDescriptions,
  playerHistories: state.events.playerHistories,
  playersPlaying: state.events.playersPlaying,
  relevantPlayerTeamsSelector: relevantPlayerTeamsSelector(state),
  relevantSeasonStats: relevantPlayerBoxScoreHistoriesSelector(state),
  relevantPlayersGameStats: relevantPlayersSelector(state),
  multipartEvents: state.eventsMultipart.events,
  watchablePlayers: state.eventsMultipart.watchablePlayers,
});

/**
 * Renders the lineup of players on the left/right hand side of the live section.
 */
const LiveLineup = React.createClass({

  propTypes: {
    actions: React.PropTypes.object.isRequired,
    contest: React.PropTypes.object,
    draftGroupStarted: React.PropTypes.bool.isRequired,
    lineup: React.PropTypes.object.isRequired,
    multipartEvents: React.PropTypes.object.isRequired,
    playerEventDescriptions: React.PropTypes.object.isRequired,
    playerHistories: React.PropTypes.object.isRequired,
    playersPlaying: React.PropTypes.array.isRequired,
    relevantPlayersGameStats: React.PropTypes.object.isRequired,
    relevantPlayerTeamsSelector: React.PropTypes.object.isRequired,
    relevantSeasonStats: React.PropTypes.object.isRequired,
    watchablePlayers: React.PropTypes.object.isRequired,
    watching: React.PropTypes.object.isRequired,
    whichSide: React.PropTypes.string.isRequired,
  },

  /**
   * Update the store.watching.playerSRID to the player chosen
   * @param {string} playerSRID  Sports Radar ID of the player
   */
  setWatchingPlayer(playerSRID) {
    const { whichSide, actions } = this.props;

    if (whichSide === 'opponent') {
      actions.updateLiveMode({ opponentPlayerSRID: playerSRID });
    } else {
      actions.updateLiveMode({ myPlayerSRID: playerSRID });
    }
  },

  /**
   * Used to close the current opponent lineup. Sets up parameters to then call props.updateWatchingAndPath()
   */
  closeLineup() {
    const { watching, actions } = this.props;
    const path = `/live/${watching.sport}/lineups/${watching.myLineupId}/contests/${watching.contestId}/`;
    const changedFields = {
      opponentLineupId: null,
    };

    actions.updateWatchingAndPath(path, changedFields);
  },

  /**
   * Render the close lineup element
   *
   * @return {JSXElement}
   */
  renderCloseLineup() {
    // you cannot close your own lineup
    if (this.props.whichSide === 'mine') {
      return (<span />);
    }

    return (
      <span className="live-lineup__close" onClick={this.closeLineup}></span>
    );
  },

  /**
   * Renders the list of players
   *
   * @return {JSXElement}
   */
  renderPlayers() {
    const { watching, contest } = this.props;
    const watchingSRID = (this.props.whichSide === 'mine') ? watching.myPlayerSRID : watching.opponentPlayerSRID;

    const renderedPlayers = this.props.lineup.roster.map((playerId) => {
      const player = this.props.lineup.rosterDetails[playerId];
      const playerSRID = player.srid;
      const isWatching = watchingSRID === playerSRID;
      const isPlaying = this.props.playersPlaying.indexOf(playerSRID) !== -1;
      const eventDescription = this.props.playerEventDescriptions[playerSRID] || {};
      const playerImagesBaseUrl = `${window.dfs.playerImagesBaseUrl}/${this.props.watching.sport}/120`;
      const gameStats = this.props.relevantPlayersGameStats[playerSRID] || {};

      let multipartEvent = {};
      let isWatchable = false;
      let playerType = '';

      if (this.props.watchablePlayers[playerSRID]) {
        const eventSrid = this.props.watchablePlayers[playerSRID];
        multipartEvent = this.props.multipartEvents[eventSrid];

        if (multipartEvent.runnerIds.indexOf(playerSRID) !== -1) {
          playerType = 'runner';
        } else {
          if (multipartEvent.hitter.sridPlayer === playerSRID) {
            playerType = 'hitter';
          } else if (multipartEvent.pitcher.sridPlayer === playerSRID) {
            playerType = 'pitcher';
          }
        }

        if (['hitter', 'pitcher'].indexOf(playerType) !== -1) {
          isWatchable = true;
        }
      }

      // hacky way to get ownership %, need to clean this up and put into selector
      if (contest && 'isLoading' in contest && !contest.isLoading && 'playersOwnership' in contest) {
        player.ownershipPercent = contest.playersOwnership.allByPlayerId[player.id];
      }

      return (
        <LiveLineupPlayer
          draftGroupStarted={this.props.draftGroupStarted}
          eventDescription={eventDescription}
          gameStats={gameStats}
          isPlaying={isPlaying}
          isWatchable={isWatchable}
          isWatching={isWatching}
          playerType={playerType}
          key={playerId}
          multipartEvent={multipartEvent}
          player={player}
          playerImagesBaseUrl={playerImagesBaseUrl}
          setWatchingPlayer={this.setWatchingPlayer}
          sport={this.props.watching.sport}
          whichSide={this.props.whichSide}
        />
      );
    }, this);

    return (
      <div className="live-lineup__players">
        {this.renderCloseLineup()}
        <ul className="live-lineup__players-list">
          {renderedPlayers}
        </ul>
      </div>
    );
  },

  render() {
    // don't show until there's a roster
    if (this.props.lineup.hasOwnProperty('roster') === false || this.props.lineup.roster.length === 0) {
      return (<div />);
    }

    const className = `live__lineup live-lineup live-lineup--${this.props.whichSide}`;

    return (
      <div className={className}>
        {this.renderPlayers()}
      </div>
    );
  },
});

// Set up Redux connections to React
const { connect } = ReactRedux;

// Wrap the component to inject dispatch and selected state into it.
export default connect(
  mapStateToProps,
  mapDispatchToProps
)(LiveLineup);
