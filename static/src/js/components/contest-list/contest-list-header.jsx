"use strict";

var React = require('react');
var Reflux = require('reflux');
var ContestStore = require("../../stores/contest-store.js");
var renderComponent = require('../../lib/render-component');
var ContestActions = require('../../actions/contest-actions.js');

/**
 * Render the header for a contest list - Displays currently active filters.
 */
var ContestListHeader = React.createClass({

  mixins: [
    Reflux.connect(ContestStore)
  ],

  revealFilters: function() {
    ContestActions.contestTypeFiltered();
  },

  render: function() {
    // Determine the contest type filter title.
    var currentLeague;
    if (ContestStore.data.activeFilters.hasOwnProperty('leagueFilter')) {
      currentLeague = (
        <span>
          <span className="cmp-contest-list__header-league">
            {ContestStore.data.activeFilters.leagueFilter.title} Contests
          </span>
          <span className="cmp-contest-list__header-divider">/</span>
        </span>
      );
    }
    if (!currentLeague || ContestStore.data.activeFilters.leagueFilter.title === 'All') {
      currentLeague = '';
    }

    // Determine the league filter title.
    var currentContestType;
    if (ContestStore.data.activeFilters.hasOwnProperty('contestTypeFilter')) {
      currentContestType = ContestStore.data.activeFilters.contestTypeFilter.title;
    }
    if (!currentContestType || currentContestType === 'All') {
      currentContestType = 'All Upcoming';
    }

    return (
      <div className="cmp-contest-list__header" onClick={this.revealFilters}>
        <h2>
          {currentLeague}
          <span className="cmp-contest-list__header-type">{currentContestType}</span>
        </h2>
      </div>
    );
  }

});


// Render the component.
renderComponent(<ContestListHeader />, '.cmp-contest-list-header');


module.exports = ContestListHeader;
