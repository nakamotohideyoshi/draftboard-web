import React from 'react'
var ContestListRow = require('./contest-list-row.jsx')
var KeypressActions = require('../../actions/keypress-actions')
import { forEach as _forEach } from 'lodash'


/**
 * Render a list (table) of contests.
 */
const ContestList = React.createClass({

  propTypes: {
    contests: React.PropTypes.array,
    focusedContestId: React.PropTypes.number,
    enterContest: React.PropTypes.func,
    setFocusedContest: React.PropTypes.func
  },


  componentDidMount: function() {
    // Listen to j/k keypress actions to focus contests.
    // KeypressActions.keypressJ.listen(this.focusNextRow);
    // KeypressActions.keypressK.listen(this.focusPreviousRow);
  },


  /**
   * When a row is clicked (or something else) we want to make that contest the 'focused' one.
   * @param {integer} id the ID of the contest to be focused.
   */
  setContestFocus: function(id) {
    if (id !== 'undefined') {
      // ContestActions.contestFocused(id);
    }
  },


  sortList: function(property) {
    // ContestActions.setSortProperty(property);
  },


  getFeaturedContests: function() {
    return (
      <tr>
        <td colSpan="7" className="featured-contests">
          <div className="featured-contests--contest">
            <img src="/static/src/img/temp/featured-contest.png" />
          </div>
          <div className="featured-contests--contest">
            <img src="/static/src/img/temp/featured-contest.png" />
          </div>
          <div className="featured-contests--contest">
            <img src="/static/src/img/temp/featured-contest.png" />
          </div>
        </td>
      </tr>
    )
  },


  render: function() {
    let featuredContests = this.getFeaturedContests()
    var visibleRows = [];

    // Build up a list of rows to be displayed.
    _forEach(this.props.contests, function(row) {
      visibleRows.push(
        <ContestListRow
            key={row.id}
            row={row}
            focusedContestId={this.props.focusedContestId}
            enterContest={this.props.enterContest}
            setFocusedContest={this.props.setFocusedContest}
        />
      )
    }, this);

    return (
      <table className="cmp-contest-list__table table">
        <thead>
          <tr className="cmp-contest-list__header-row">
            <th
              className="table__sortable"
              onClick={this.sortList.bind(this, 'sport')}></th>
            <th
              className="table__sortable"
              onClick={this.sortList.bind(this, 'name')}>Contest</th>
            <th
              className="table__sortable"
              onClick={this.sortList.bind(this, 'entries')}>Entries / Size</th>
            <th
              className="table__sortable"
              onClick={this.sortList.bind(this, 'buyin')}>Fee</th>
            <th
              className="table__sortable"
              onClick={this.sortList.bind(this, 'prize_pool')}>Prizes</th>
            <th
              className="table__sortable"
              onClick={this.sortList.bind(this, 'start')}>Live In</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {featuredContests}
          {visibleRows}
        </tbody>
      </table>
    );
  }

});


module.exports = ContestList;
