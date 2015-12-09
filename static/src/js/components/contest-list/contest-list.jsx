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
    focusedContest: React.PropTypes.object,
    focusedLineup: React.PropTypes.object.isRequired,
    hoveredLineupId: React.PropTypes.number,
    enterContest: React.PropTypes.func,
    setFocusedContest: React.PropTypes.func,
    setOrderBy: React.PropTypes.func,
    draftGroupsWithLineups: React.PropTypes.array,
    lineupsInfo: React.PropTypes.object
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


  getFeaturedContests: function() {
    return (
      <tr className="featured-contests">
        <td colSpan="7">
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
      let isEntered = false
      let isHoveredEntered = false
      let info = {}

      if (this.props.lineupsInfo.hasOwnProperty(this.props.focusedLineup.id)) {
        info = this.props.lineupsInfo[this.props.focusedLineup.id]
        isEntered = (info.contests.indexOf(row.id) != -1)
      }

      if(this.props.lineupsInfo.hasOwnProperty(this.props.hoveredLineupId)) {
        info = this.props.lineupsInfo[this.props.hoveredLineupId]
        isHoveredEntered = (info.contests.indexOf(row.id) != -1)
      }

      visibleRows.push(
        <ContestListRow
            key={row.id}
            row={row}
            isEntered={isEntered}
            highlighted={isHoveredEntered}
            focusedContest={this.props.focusedContest}
            focusedLineup={this.props.focusedLineup}
            enterContest={this.props.enterContest}
            setFocusedContest={this.props.setFocusedContest}
            draftGroupsWithLineups={this.props.draftGroupsWithLineups}
        />
      )
    }, this);

    return (
      <table className="cmp-contest-list cmp-contest-list__table table">
        <thead>
          <tr className="cmp-contest-list__header-row">
            <th
              className="table__sortable"
              onClick={this.props.setOrderBy.bind(null, 'sport')}></th>
            <th
              className="table__sortable"
              onClick={this.props.setOrderBy.bind(null, 'name')}>Contest</th>
            <th
              className="table__sortable"
              onClick={this.props.setOrderBy.bind(null, 'entries')}>Entries / Size</th>
            <th
              className="table__sortable"
              onClick={this.props.setOrderBy.bind(null, 'buyin')}>Fee</th>
            <th
              className="table__sortable"
              onClick={this.props.setOrderBy.bind(null, 'prize_pool')}>Prizes</th>
            <th
              className="table__sortable"
              onClick={this.props.setOrderBy.bind(null, 'start')}>Live In</th>
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
