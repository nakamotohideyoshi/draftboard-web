import React from 'react';
import ReactRedux from 'react-redux';
import store from '../../store';
import LineupCard from '../lineup/lineup-card.jsx';
import DraftNewLineupCard from './draft-new-lineup-card.jsx';
import renderComponent from '../../lib/render-component';
import * as AppActions from '../../stores/app-state-store.js';
import { lineupsByDraftGroupSelector } from '../../selectors/upcoming-lineups-by-draftgroup.js';
import { setFocusedPlayer } from '../../actions/draft-group-players-actions.js';
import { importLineup, saveLineup, saveLineupEdit, removePlayer, createLineupInit, }
  from '../../actions/lineup-actions.js';
import { map as _map } from 'lodash';
import { Router, Route } from 'react-router';
import { syncReduxAndRouter } from 'redux-simple-router';
import createBrowserHistory from 'history/lib/createBrowserHistory';

const history = createBrowserHistory();
const { Provider, connect } = ReactRedux;
syncReduxAndRouter(history, store);


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


  render() {
    const lineups = _map(this.props.lineups, (lineup) => {
      const refName = `lineup-${lineup.id}`;
      return (
        <LineupCard
          key={lineup.id}
          lineup={lineup}
          isActive={false}
          ref={refName}
          onCardClick={this.handleCardClick}
          hoverText="Import Lineup"
        />
      );
    }, this);

    return (
      <div>
        <DraftNewLineupCard
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
        />

        {lineups}
      </div>
    );
  },
});


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
