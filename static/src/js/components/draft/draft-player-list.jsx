'use strict';

var React = require('react');
var Reflux = require('reflux');
var ContestStore = require("../../stores/contest-store.js");
var DraftGroupStore = require("../../stores/draft-group-store.js");
var DraftNewLineupStore = require("../../stores/draft-new-lineup-store.js");
var renderComponent = require('../../lib/render-component');
var ContestStorePropertyMatchFilter = require('../contest-list/contest-store-property-match-filter.jsx');
var ContestListSearchFilter = require('../contest-list/contest-list-search-filter.jsx');
var ContestListFeeFilter = require('../contest-list/contest-list-fee-filter.jsx');
var PlayerListRow = require('./draft-player-list-row.jsx');
// var ContestListDetail = require('../contest-list/contest-list-detail.jsx');
var KeypressActions = require('../../actions/keypress-actions');
var ContestActions = require('../../actions/contest-actions');
var DraftActions = require("../../actions/draft-actions");
require('../contest-list/contest-list-header.jsx');
require('../contest-list/contest-list-detail.jsx');
require('../contest-list/contest-list-sport-filter.jsx');


/**
 * Render a list of players able to be drafted.
 */
var DraftPlayerList = React.createClass({

  mixins: [
    Reflux.connect(DraftGroupStore),
    Reflux.connect(DraftNewLineupStore, 'newLineup')
  ],


  getInitialState: function() {
    DraftActions.loadDraftGroup(3);

    return ({
      players: [],
      filteredPlayers: [],
      // Contest type filter data.
      contestTypeFilters: [
        {title: 'All', column: 'contestType', match: ''},
        {title: 'Guaranteed', column: 'contestType', match: 'gpp'},
        {title: 'Double-Up', column: 'contestType', match: 'double-up'},
        {title: 'Heads-Up', column: 'contestType', match: 'h2h'}
      ],
      newLineup: {
        availablePositions: []
      }
    });
  },


  /**
   * When a row is clicked (or something else) we want to make that contest the 'focused' one.
   * @param {integer} id the ID of the contest to be focused.
   */
  setContestFocus: function(id) {
    if (id !== 'undefined') {
      ContestActions.contestFocused(id);
    }
  },

  onPlayerClick: function(playerId) {
    DraftActions.addPlayerToLineup(playerId);
  },


  componentWillMount: function() {
    // Listen to j/k keypress actions to focus contests.
    KeypressActions.keypressJ.listen(this.focusNextRow);
    KeypressActions.keypressK.listen(this.focusPreviousRow);
  },


  /**
   * Focus the next visible row in the contest list and open the detail pane.
   */
  focusNextRow: function() {
    this.setContestFocus(ContestStore.getNextVisibleRowId());
  },


  /**
   * Focus the previous row in the contest list and open the detail pane.
   */
  focusPreviousRow: function() {
    this.setContestFocus(ContestStore.getPreviousVisibleRowId());
  },


  render: function() {
    // Build up a list of rows to be displayed.
    var visibleRows = this.state.players.map(function(row) {
      var draftable = true;



      if (this.state.newLineup.availablePositions.indexOf(row.position) === -1) {
        draftable = false;
      }

      return (
        <PlayerListRow
          key={row.player_id}
          row={row}
          draftable={draftable}
          handleOnClick={this.onPlayerClick}
          focusedContestId={this.state.focusedContestId} />
      );
    }, this);


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

        <table className="cmp-contest-list__table table">
          <thead>
            <tr className="cmp-contest-list__header-row">
              <th>POS</th>
              <th>Player</th>
              <th>Status</th>
              <th>OPP</th>
              <th>FPPG</th>
              <th>Salary</th>
              <th></th>
            </tr>
          </thead>
          <tbody>{visibleRows}</tbody>
        </table>
      </div>
    );
  }

});


// Render the component.
renderComponent(<DraftPlayerList />, '.cmp-draft-player-list');


module.exports = DraftPlayerList;
