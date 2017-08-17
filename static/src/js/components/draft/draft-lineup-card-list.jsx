import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import DraftNewLineupCard from './draft-new-lineup-card';
import renderComponent from '../../lib/render-component';
import * as AppActions from '../../stores/app-state-store';
import { lineupsByDraftGroupSelector } from '../../selectors/upcoming-lineups-by-draftgroup';
import { setFocusedPlayer, updateFilter } from '../../actions/draft-group-players-actions';
import { importLineup, saveLineup, saveLineupEdit, removePlayer, createLineupInit }
  from '../../actions/upcoming-lineup-actions';
import { Router, Route, browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux';
import { activeDraftGroupBoxScoresSelector } from '../../selectors/draft-group-info-selector';
import { upcomingLineupsInfo } from '../../selectors/upcoming-lineups-info';
import playerPositionFilterData from '../filters/player-position-filter-data';
import find from 'lodash/find';


/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
function mapStateToProps(state) {
  return {
    // allLineups: state.upcomingLineups.lineups,
    lineups: lineupsByDraftGroupSelector(state),
    newLineup: state.createLineup,
    sport: state.draftGroupPlayers.sport,
    draftGroupId: state.draftGroupPlayers.id,
    draftGroupBoxScores: activeDraftGroupBoxScoresSelector(state),
    lineupsInfo: upcomingLineupsInfo(state),
    draftGroupStart: state.draftGroupPlayers.start,
  };
}

/*
 * Map Redux actions to React component properties
 * @param  {function} dispatch The dispatch method to pass actions into
 * @return {object}            All of the methods to map to the component
 */
function mapDispatchToProps(dispatch) {
  return {
    createLineupInit: (sport) => dispatch(createLineupInit(sport)),
    removePlayer: (playerId) => dispatch(removePlayer(playerId)),
    saveLineup: (lineup, title, draftGroupId) => dispatch(saveLineup(lineup, title, draftGroupId)),
    saveLineupEdit: (lineup, title, lineupId) => dispatch(saveLineupEdit(lineup, title, lineupId)),
    importLineup: (lineup) => dispatch(importLineup(lineup)),
    setFocusedPlayer: (playerId) => dispatch(setFocusedPlayer(playerId)),
    updateFilter: (filterName, filterProperty, match) => dispatch(
      updateFilter(filterName, filterProperty, match)),
  };
}


/**
 * Renders a list of lineup cards on the draft screen. Feed it lineup data and it will render
 * a collapsed LineupCard component for each lineup.
 */
const DraftLineupCardList = React.createClass({

  propTypes: {
    lineups: React.PropTypes.oneOfType([
      React.PropTypes.array,
      React.PropTypes.object,
    ]),
    newLineup: React.PropTypes.object.isRequired,
    createLineupInit: React.PropTypes.func.isRequired,
    removePlayer: React.PropTypes.func.isRequired,
    sport: React.PropTypes.string,
    draftGroupId: React.PropTypes.number,
    saveLineup: React.PropTypes.func,
    saveLineupEdit: React.PropTypes.func,
    importLineup: React.PropTypes.func,
    params: React.PropTypes.object,
    setFocusedPlayer: React.PropTypes.func,
    draftGroupBoxScores: React.PropTypes.object,
    lineupsInfo: React.PropTypes.object,
    draftGroupStart: React.PropTypes.string,
    updateFilter: React.PropTypes.func.isRequired,
  },


  getDefaultProps() {
    return {
      lineups: [],
      newLineup: {
        lineup: [],
      },
    };
  },


  componentWillMount() {
    if (this.props.sport) {
      this.props.createLineupInit(this.props.sport);
    }
  },


  componentWillReceiveProps(nextProps) {
    // If we get new props, and a new sport is passed (meaning a new draftgroup has been loaded)
    // initializes a new lineup creation card.
    if (nextProps.sport !== this.props.sport) {
      this.props.createLineupInit(nextProps.sport);
    }
  },


  handlePlayerClick(playerId) {
    this.props.setFocusedPlayer(playerId);
    AppActions.openPane();
  },

  /**
   * When one of the empty slot "Select a Running back" gets clicked, change the player position
   * filter to match that slot position.
   *
   * @param position String
   */
  handleEmtpySlotClick(position) {
    const sportFilters = playerPositionFilterData[this.props.sport];
    const filter = find(sportFilters, { title: position });
    this.props.updateFilter('positionFilter', filter.column, filter.match);
  },

  /**
   * Click handler for a lineupCard - imports the clicked lineup onto the new one.
   */
  handleCardClick(lineup) {
    this.props.importLineup(lineup);
  },


  handleSaveLineup(title) {
    if (this.props.params.lineupAction === 'edit') {
      this.props.saveLineupEdit(this.props.newLineup.lineup, title, this.props.params.lineupId);
    } else {
      this.props.saveLineup(this.props.newLineup.lineup, title, this.props.draftGroupId);
    }
  },


  isLineupBeingSaved() {
    // TODO: this breaks when not editing a lineup. Dump this idea and figure out a better way to handle it.
    //
    // const currentLineup = find(this.props.lineups, (lineup) =>
    //   lineup.id.toString() === this.props.params.lineupId.toString()
    // );
    // if (currentLineup) {
    //   return currentLineup.isSaving;
    // }
    //
    return false;
  },


  render() {
    return (
      <div>
        <DraftNewLineupCard
          isSaving={this.isLineupBeingSaved()}
          lineup={this.props.newLineup.lineup}
          lineupTitle={this.props.newLineup.lineupTitle}
          lineupCanBeSaved={this.props.newLineup.lineupCanBeSaved}
          isActive={false}
          ref="lineupCardNew"
          remainingSalary={this.props.newLineup.remainingSalary}
          avgRemainingPlayerSalary={this.props.newLineup.avgRemainingPlayerSalary}
          errorMessage={this.props.newLineup.errorMessage}
          removePlayer={this.props.removePlayer}
          saveLineup={this.handleSaveLineup}
          handlePlayerClick={this.handlePlayerClick}
          sport={this.props.sport}
          draftGroupBoxScores={this.props.draftGroupBoxScores}
          draftGroupStart={this.props.draftGroupStart}
          handleEmtpySlotClick={this.handleEmtpySlotClick}
        />
      </div>
    );
  },
});

// Set up Redux connections to React
const { Provider, connect } = ReactRedux;

// Create an enhanced history that syncs navigation events with the store
const history = syncHistoryWithStore(browserHistory, store);

// Wrap the component to inject dispatch and selected state into it.
const DraftLineupCardListConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(DraftLineupCardList);

// Render the component.
renderComponent(
  <Provider store={store}>
      <Router history={history}>
        <Route path="/draft/:draftgroupId/" component={DraftLineupCardListConnected} />
        <Route path="/draft/:draftgroupId/lineup/:lineupId/:lineupAction" component={DraftLineupCardListConnected} />
      </Router>
  </Provider>,
  '.cmp-draft-lineup-card-list'
);


module.exports = DraftLineupCardList;
