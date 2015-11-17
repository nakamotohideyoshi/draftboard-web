const React = require('react');
const ReactRedux = require('react-redux');
const store = require('../../store');
var LineupCard = require('../lineup/lineup-card.jsx');
var DraftNewLineupCard = require('./draft-new-lineup-card.jsx');
var renderComponent = require('../../lib/render-component');
import {importLineup, saveLineup, removePlayer, fetchUpcomingLineups, createLineupInit
  } from '../../actions/lineup-actions.js';
var log = require("../../lib/logging");


/**
 * Renders a list of lineup cards on the draft screen. Feed it lineup data and it will render
 * a collapsed LineupCard component for each lineup.
 */
var DraftLineupCardList = React.createClass({

  propTypes: {
    fetchUpcomingLineups: React.PropTypes.func.isRequired,
    lineups: React.PropTypes.array.isRequired,
    newLineup: React.PropTypes.object.isRequired,
    createLineupInit: React.PropTypes.func.isRequired,
    removePlayer: React.PropTypes.func.isRequired,
    sport: React.PropTypes.string,
    draftGroupId: React.PropTypes.number,
    saveLineup: React.PropTypes.func,
    importLineup: React.PropTypes.func
  },


  componentWillMount: function() {
    this.props.fetchUpcomingLineups();

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
    this.props.saveLineup(this.props.newLineup.lineup, title, this.props.draftGroupId)
  },


  render: function() {
    var lineups = this.props.lineups.map(function(lineup) {
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
    lineups: state.upcomingLineups.lineups,
    newLineup: state.createLineup,
    sport: state.draftDraftGroup.sport,
    draftGroupId: state.draftDraftGroup.id
  };
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    fetchUpcomingLineups: () => dispatch(fetchUpcomingLineups()),
    createLineupInit: (sport) => dispatch(createLineupInit(sport)),
    removePlayer: (playerId) => dispatch(removePlayer(playerId)),
    saveLineup: (lineup, title, draftGroupId) => dispatch(saveLineup(lineup, title, draftGroupId)),
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
    <DraftLineupCardListConnected />
  </Provider>,
  '.cmp-draft-lineup-card-list'
);


module.exports = DraftLineupCardList;
