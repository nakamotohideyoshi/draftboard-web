const React = require('react');
const ReactRedux = require('react-redux');
const store = require('../../store');
var LineupCard = require('../lineup/lineup-card.jsx');
var DraftNewLineupCard = require('./draft-new-lineup-card.jsx');
var renderComponent = require('../../lib/render-component');
import {LineupsByDraftGroupSelector} from '../../selectors/upcoming-lineups-by-draftgroup.js'
import {importLineup, saveLineup, saveLineupEdit, removePlayer, fetchUpcomingLineups,
  createLineupInit, createLineupViaCopy} from '../../actions/lineup-actions.js';
var log = require("../../lib/logging");
import {map as _map} from 'lodash'
import { Router, Route } from 'react-router'
import {updatePath, syncReduxAndRouter} from 'redux-simple-router'
import createBrowserHistory from 'history/lib/createBrowserHistory'

const history = createBrowserHistory()
syncReduxAndRouter(history, store)


/**
 * Renders a list of lineup cards on the draft screen. Feed it lineup data and it will render
 * a collapsed LineupCard component for each lineup.
 */
var DraftLineupCardList = React.createClass({

  propTypes: {
    lineups: React.PropTypes.oneOfType([
      React.PropTypes.array,
      React.PropTypes.object
    ]),
    newLineup: React.PropTypes.object.isRequired,
    createLineupInit: React.PropTypes.func.isRequired,
    removePlayer: React.PropTypes.func.isRequired,
    sport: React.PropTypes.string,
    draftGroupId: React.PropTypes.number,
    saveLineup: React.PropTypes.func,
    saveLineupEdit: React.PropTypes.func,
    importLineup: React.PropTypes.func,
    params: React.PropTypes.object
  },


  componentWillMount: function() {
    if (this.props.sport) {
      this.props.createLineupInit(this.props.sport);
    }
  },


  componentWillReceiveProps: function(nextProps) {
    // If we get new props, and a new sport is passed (meaning a new draftgroup has been loaded)
    // initializes a new lineup creation card.
    if (nextProps.sport !== this.props.sport) {
      this.props.createLineupInit(nextProps.sport);
    }
  },


  getDefaultProps: function() {
    return {
      lineups: [],
      newLineup: {
        lineup: []
      }
    };
  },



  /**
   * Click handler for a lineupCard - imports the clicked lineup onto the new one.
   */
  handleCardClick: function(lineup) {
    this.props.importLineup(lineup);
  },


  handleSaveLineup: function(title) {
    if (this.props.params.action === 'edit') {
      this.props.saveLineupEdit(this.props.newLineup.lineup, title, this.props.params.lineupId)
    } else {
      this.props.saveLineup(this.props.newLineup.lineup, title, this.props.draftGroupId)
    }

  },


  render: function() {
    var lineups = _map(this.props.lineups, function(lineup) {
      var refName = 'lineup-' + lineup.id;
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
          isActive={false}
          ref="lineupCardNew"
          remainingSalary={this.props.newLineup.remainingSalary}
          avgPlayerSalary={this.props.newLineup.avgPlayerSalary}
          errorMessage={this.props.newLineup.errorMessage}
          removePlayer={this.props.removePlayer}
          saveLineup={this.handleSaveLineup}
        />

        {lineups}
      </div>
    );
  }
});


// Redux integration
let {Provider, connect} = ReactRedux;

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {
    // allLineups: state.upcomingLineups.lineups,
    lineups: LineupsByDraftGroupSelector(state),
    newLineup: state.createLineup,
    sport: state.draftDraftGroup.sport,
    draftGroupId: state.draftDraftGroup.id
  };
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    createLineupInit: (sport) => dispatch(createLineupInit(sport)),
    removePlayer: (playerId) => dispatch(removePlayer(playerId)),
    saveLineup: (lineup, title, draftGroupId) => dispatch(saveLineup(lineup, title, draftGroupId)),
    saveLineupEdit: (lineup, title, lineupId) => dispatch(saveLineupEdit(lineup, title, lineupId)),
    importLineup: (lineup) => dispatch(importLineup(lineup))
  };
}

// Wrap the component to inject dispatch and selected state into it.
var DraftLineupCardListConnected = connect(
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
