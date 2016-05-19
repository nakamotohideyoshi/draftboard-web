import LiveOverallStats from './live-overall-stats';
import React from 'react';


/**
 * Return the header section of the live page, including the lineup/contest title and overall stats
 */
const LiveHeader = (props) => {
  const { myLineup, contest, opponentLineup, watching } = props;

  // set all needed variables, and default them to lineup only
  let opponentStats;
  let primary = myLineup.name;
  let statsVs;
  let hasContest = false;

  // if watching a contest, then update the titles and ensure the overall stats are contest-based
  if (watching.contestId !== null && !contest.isLoading) {
    hasContest = true;
    primary = myLineup.name;

    // if watching an opponent, then add in second overall stats and update the titles
    if (watching.opponentLineupId !== null && !opponentLineup.isLoading) {
      statsVs = (
        <div className="live-overall-stats__vs">vs</div>
      );
      opponentStats = (
        <LiveOverallStats
          contest={contest}
          hasContest
          lineup={opponentLineup}
          whichSide="opponent"
        />
      );
    }
  }

  return (
    <header className="cmp-live__scoreboard live-scoreboard">
      <h1 className="live-scoreboard__contest-name">
        {primary}
      </h1>

      <LiveOverallStats
        contest={contest}
        lineup={myLineup}
        hasContest={hasContest}
        whichSide="mine"
      />

      {statsVs}
      {opponentStats}
    </header>
  );
};

LiveHeader.propTypes = {
  contest: React.PropTypes.object.isRequired,
  myLineup: React.PropTypes.object.isRequired,
  opponentLineup: React.PropTypes.object.isRequired,
  watching: React.PropTypes.object.isRequired,
};

export default LiveHeader;
