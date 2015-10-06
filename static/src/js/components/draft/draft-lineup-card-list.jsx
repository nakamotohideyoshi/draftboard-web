'use strict';

var React = require('react');
var Reflux = require('reflux');
var LineupCard = require('../lineup/lineup-card.jsx');
var DraftNewLineupCard = require('./draft-new-lineup-card.jsx');
var renderComponent = require('../../lib/render-component');
var DraftNewLineupStore = require('../../stores/draft-new-lineup-store.js');
var LineupStore = require('../../stores/lineup-store.js');
// var LineupActions = require('../../actions/lineup-actions.js');
var log = require("../../lib/logging");


/**
 * Renders a list of lineup cards on the draft screen. Feed it lineup data and it will render
 * a collapsed LineupCard component for each lineup.
 */
var DraftLineupCardList = React.createClass({

  mixins: [
    Reflux.connect(LineupStore),
    Reflux.connect(DraftNewLineupStore, 'newLineup')
  ],


  getInitialState: function() {
    return {
      lineups: [],
      newLineup: {
        lineup: []
      },
      focusedLineupId: 10
    };
  },


  importLineup: function(lineupId) {
    log.debug('DraftLineupCardList.importLineup()', lineupId);
  },


  /**
   * Click handler for a lineupCard
   * @param  {int} id The cards ID TODO: this can be removed once we have legit data.
   */
  onCardClick: function(id) {
    this.importLineup(id);
  },



  render: function() {
    var lineups = this.state.lineups.map(function(lineup) {
      var refName = 'lineup-' + lineup.id;
      return (
        <LineupCard
          key={lineup.id}
          lineup={lineup}
          isActive={false}
          ref={refName}
          onCardClick={this.onCardClick}
          hoverText="Import Lineup"
        />
      );
    }, this);

    return (
      <div>
        <DraftNewLineupCard
          lineup={this.state.newLineup.lineup}
          isActive={false}
          ref="lineupCardNew"
          remainingSalary={this.state.newLineup.remainingSalary}
          avgPlayerSalary={this.state.newLineup.avgPlayerSalary}
          errorMessage={this.state.newLineup.errorMessage}
        />

        {lineups}
      </div>
    );
  }
});

// Render the component.
renderComponent(<DraftLineupCardList />, '.cmp-draft-lineup-card-list');


module.exports = DraftLineupCardList;
