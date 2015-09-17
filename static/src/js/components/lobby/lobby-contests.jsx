'use strict';

var React = require('react');
var Reflux = require('reflux');
var ContestStore = require("../../stores/contest-store.js");
var renderComponent = require('../../lib/render-component');
var ContestStorePropertyMatchFilter = require('../contest-list/contest-store-property-match-filter.jsx');
var ContestListSearchFilter = require('../contest-list/contest-list-search-filter.jsx');
var ContestListFeeFilter = require('../contest-list/contest-list-fee-filter.jsx');
var ContestList = require('../contest-list/contest-list.jsx');
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
          <ContestStorePropertyMatchFilter
            className="contest-list-filter--contest-type"
            filters={this.state.contestTypeFilters}
            filterName="contestTypeFilter"
            property='contestType'
            match=''
          />

          <div className="contest-list-filter-set__group">
            <ContestListFeeFilter
              className="contest-list-filter--contest-fee"
              filterName="contestFeeFilter"
             />

            <ContestListSearchFilter
              className="contest-list-filter--contest-type"
              filterName="contestSearchFilter"
              property='name'
              match=''
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
