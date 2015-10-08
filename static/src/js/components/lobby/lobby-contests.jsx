'use strict';

var React = require('react');
var Reflux = require('reflux');
var ContestStore = require("../../stores/contest-store.js");
var renderComponent = require('../../lib/render-component');
var CollectionMatchFilter = require('../filters/collection-match-filter.jsx');
var CollectionSearchFilter = require('../filters/collection-search-filter.jsx');
var CollectionRangeSliderFilter = require('../filters/collection-range-slider-filter.jsx');
var ContestList = require('../contest-list/contest-list.jsx');
var ContestActions = require('../../actions/contest-actions.js');
require('../../stores/draft-groups-store.js');
require('../contest-list/contest-list-header.jsx');
require('../contest-list/contest-list-detail.jsx');
require('../contest-list/contest-list-sport-filter.jsx');


/**
 * The contest list section of the lobby.
 */
var LobbyContests = React.createClass({

  mixins: [
    Reflux.connect(ContestStore)
  ],


  getInitialState: function() {
    return ({
      filteredContests: [],
      // Contest type filter data.
      contestTypeFilters: [
        {title: 'All', column: 'contestType', match: ''},
        {title: 'Guaranteed', column: 'contestType', match: 'gpp'},
        {title: 'Double-Up', column: 'contestType', match: 'double-up'},
        {title: 'Heads-Up', column: 'contestType', match: 'h2h'}
      ]
    });
  },


  render: function() {

    return (
      <div>
        <div className="contest-list-filter-set">
          <CollectionMatchFilter
            className="contest-list-filter--contest-type"
            filters={this.state.contestTypeFilters}
            filterName="contestTypeFilter"
            filterProperty='contestType'
            match=''
            onUpdate={ContestActions.filterUpdated}
            onMount={ContestActions.registerFilter}
          />

          <div className="contest-list-filter-set__group">
            <CollectionRangeSliderFilter
              className="contest-list-filter--contest-fee"
              filterName="contestFeeFilter"
              filterProperty='fee'
              onUpdate={ContestActions.filterUpdated}
              onMount={ContestActions.registerFilter}
             />

           <CollectionSearchFilter
              className="contest-list-filter--contest-name"
              filterName="contestSearchFilter"
              filterProperty='name'
              onUpdate={ContestActions.filterUpdated}
              onMount={ContestActions.registerFilter}
            />
          </div>
        </div>

        <ContestList
          contests={this.state.filteredContests}
          focusedContestId={this.state.focusedContestId}
        />
      </div>
    );
  }

});


// Render the component.
renderComponent(<LobbyContests />, '.cmp-lobby-contests');


module.exports = LobbyContests;
