import React from 'react';
// import FeaturedContests from './featured-contests.jsx';
import ContestListRow from './contest-list-row.jsx';
import forEach from 'lodash/forEach';


/**
 * Render a list (table) of contests.
 */


const ContestList = (props) => {
  const visibleRows = [];

  if (props.isFetchingContestPools && props.contests.length === 0) {
    visibleRows.push(
      <tr key="loading"><td colSpan="8">Loading Contests</td></tr>
    );
  }

  // Build up a list of rows to be displayed.
  forEach(props.contests, (row) => {
    let isEntered = false;
    let isHoveredEntered = false;
    let info = {};

    if (props.focusedLineup && props.lineupsInfo.hasOwnProperty(props.focusedLineup.id)) {
      info = props.lineupsInfo[props.focusedLineup.id];
      isEntered = (info.contestPoolEntries.hasOwnProperty(row.id));
    }

    if (props.lineupsInfo.hasOwnProperty(props.hoveredLineupId)) {
      info = props.lineupsInfo[props.hoveredLineupId];
      isHoveredEntered = (info.contestPoolEntries.hasOwnProperty(row.id));
    }

    visibleRows.push(
      <ContestListRow
        draftGroupsWithLineups={props.draftGroupsWithLineups}
        enterContest={props.enterContest}
        focusedContest={props.focusedContest}
        focusedLineup={props.focusedLineup}
        highlighted={isHoveredEntered}
        isEntered={isEntered}
        key={row.id}
        contest={row}
        setFocusedContest={props.setFocusedContest}
        lineupsInfo={props.lineupsInfo}
        entrySkillLevels={props.entrySkillLevels}
      />
    );
  }, this);


  return (
    <table className="cmp-contest-list cmp-contest-list__table table">
      <thead>
        <tr className="cmp-contest-list__header-row">
          <th
            className="table__sortable"
            // onClick={props.setOrderBy.bind(null, 'sport')}
          >&nbsp;</th>
          <th
            className="table__sortable"
            // onClick={props.setOrderBy.bind(null, 'name')}
          >Contest Type</th>
          <th>Details</th>
          <th
            className="table__sortable"
            // onClick={props.setOrderBy.bind(null, 'prize_pool')}
          >Prizes</th>
          <th
            className="table__sortable"
            // onClick={props.setOrderBy.bind(null, 'entries')}
          >Entries</th>
          <th>My Entries</th>
          <th
            className="table__sortable"
            // onClick={props.setOrderBy.bind(null, 'start')}
          >Live In</th>

          <th>&nbsp;</th>
        </tr>
      </thead>
      <tbody>
        {visibleRows}
      </tbody>
    </table>
  );
};

ContestList.propTypes = {
  contests: React.PropTypes.array,
  draftGroupsWithLineups: React.PropTypes.array,
  enterContest: React.PropTypes.func,
  focusedContest: React.PropTypes.object,
  focusedLineup: React.PropTypes.object,
  hoveredLineupId: React.PropTypes.number,
  lineupsInfo: React.PropTypes.object,
  setFocusedContest: React.PropTypes.func,
  setOrderBy: React.PropTypes.func,
  entrySkillLevels: React.PropTypes.object.isRequired,
  isFetchingContestPools: React.PropTypes.bool.isRequired,
};


module.exports = ContestList;
