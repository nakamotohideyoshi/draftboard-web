import React from 'react';
import FeaturedContests from './featured-contests.jsx';
import ContestListRow from './contest-list-row.jsx';
import { forEach as _forEach } from 'lodash';


/**
 * Render a list (table) of contests.
 */
const ContestList = React.createClass({

  propTypes: {
    contests: React.PropTypes.array,
    draftGroupsWithLineups: React.PropTypes.array,
    enterContest: React.PropTypes.func,
    featuredContests: React.PropTypes.array.isRequired,
    focusedContest: React.PropTypes.object,
    focusedLineup: React.PropTypes.object,
    hoveredLineupId: React.PropTypes.number,
    lineupsInfo: React.PropTypes.object,
    setFocusedContest: React.PropTypes.func,
    setOrderBy: React.PropTypes.func,
  },


  componentDidMount() {
    // Listen to j/k keypress actions to focus contests.
    // KeypressActions.keypressJ.listen(this.focusNextRow);
    // KeypressActions.keypressK.listen(this.focusPreviousRow);
  },


  render() {
    const visibleRows = [];

    // Build up a list of rows to be displayed.
    _forEach(this.props.contests, (row) => {
      let isEntered = false;
      let isHoveredEntered = false;
      let info = {};

      if (this.props.focusedLineup && this.props.lineupsInfo.hasOwnProperty(this.props.focusedLineup.id)) {
        info = this.props.lineupsInfo[this.props.focusedLineup.id];
        isEntered = (info.contestPoolEntries.indexOf(row.id) !== -1);
      }

      if (this.props.lineupsInfo.hasOwnProperty(this.props.hoveredLineupId)) {
        info = this.props.lineupsInfo[this.props.hoveredLineupId];
        isHoveredEntered = (info.contestPoolEntries.indexOf(row.id) !== -1);
      }

      visibleRows.push(
        <ContestListRow
          draftGroupsWithLineups={this.props.draftGroupsWithLineups}
          enterContest={this.props.enterContest}
          focusedContest={this.props.focusedContest}
          focusedLineup={this.props.focusedLineup}
          highlighted={isHoveredEntered}
          isEntered={isEntered}
          key={row.id}
          contest={row}
          setFocusedContest={this.props.setFocusedContest}
          lineupsInfo={this.props.lineupsInfo}
        />
      );
    }, this);

    return (
      <table className="cmp-contest-list cmp-contest-list__table table">
        <thead>
          <tr className="cmp-contest-list__header-row">
            <th
              className="table__sortable"
              onClick={this.props.setOrderBy.bind(null, 'sport')}
            ></th>
            <th
              className="table__sortable"
              onClick={this.props.setOrderBy.bind(null, 'name')}
            >Contest</th>
            <th
              className="table__sortable"
              onClick={this.props.setOrderBy.bind(null, 'entries')}
            >Entries / Size</th>
            <th
              className="table__sortable"
              onClick={this.props.setOrderBy.bind(null, 'buyin')}
            >Fee</th>
            <th
              className="table__sortable"
              onClick={this.props.setOrderBy.bind(null, 'prize_pool')}
            >Prizes</th>
            <th
              className="table__sortable"
              onClick={this.props.setOrderBy.bind(null, 'start')}
            >Live In</th>
            <th>Max Entries</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr className="featured-contests">
            <td colSpan="8">
              <FeaturedContests featuredContests={this.props.featuredContests} />
            </td>
          </tr>
          {visibleRows}
        </tbody>
      </table>
    );
  },

});


module.exports = ContestList;
