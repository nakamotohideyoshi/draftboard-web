'use strict';

var React = require('react');
var renderComponent = require('../../lib/render-component');
var CollectionMatchFilter = require('../filters/collection-match-filter.jsx');
var ContestActions = require('../../actions/contest-actions.js');


/**
 * A league filter for a ContestList DataTable - This sits above the lineup cards in the sidebar.
 */
var ContestListSportFilter = React.createClass({

  getInitialState: function() {
    return {
      // League filter data - these will likely be replaced by dynamically determined values.
      leagueFilters: [
        {title: 'All', column: 'sport', match: ''},
        {title: 'NBA', column: 'sport', match: 'nba'},
        {title: 'NFL', column: 'sport', match: 'nfl'},
        {title: 'MLB', column: 'sport', match: 'mlb'}
      ]
    };
  },

  render: function() {
    return (
        <CollectionMatchFilter
          className="contest-list-filter--sport"
          filters={this.state.leagueFilters}
          filterProperty='sport'
          match=''
          filterName='sportFilter'
          onUpdate={ContestActions.filterUpdated}
          onMount={ContestActions.registerFilter}
        />
    );
  }

});


// Render the component.
renderComponent(<ContestListSportFilter />, '.cmp-contest-list-sport-filter');


module.exports = ContestListSportFilter;
