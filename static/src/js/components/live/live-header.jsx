import LiveOverallStats from './live-overall-stats';
import React from 'react';

// assets
require('../../../sass/blocks/live/live-header.scss');


/**
 * Return the header section of the live page, including the lineup/contest title and overall stats
 */
const LiveHeader = (props) => {
  const { myLineup, contest, opponentLineup, watching } = props;

  // show nothing if loading
  if (myLineup.isLoading !== false) return null;

  // set all needed variables, and default them to lineup only
  let opponentStats;
  let statsVs;
  let { potentialWinnings, rank } = myLineup;

  // if watching a contest, then update the titles and ensure the overall stats are contest-based
  if (watching.contestId !== null && contest.isLoading === false) {
    potentialWinnings = contest.potentialWinnings;
    rank = contest.rank;

    // if watching an opponent, then add in second overall stats and update the titles
    if (watching.opponentLineupId !== null && opponentLineup.isLoading === false) {
      statsVs = (
        <div className="live-overall-stats__vs">vs</div>
      );
      opponentStats = (
        <LiveOverallStats
          fp={opponentLineup.fp}
          id={opponentLineup.id}
          name={opponentLineup.name}
          potentialWinnings={potentialWinnings}
          rank={rank}
          timeRemaining={opponentLineup.timeRemaining}
          whichSide="opponent"
        />
      );
    }
  }

  return (
    <header className="live-header">
      <LiveOverallStats
        fp={myLineup.fp}
        id={myLineup.id}
        name={myLineup.name}
        potentialWinnings={potentialWinnings}
        rank={rank}
        timeRemaining={myLineup.timeRemaining}
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
