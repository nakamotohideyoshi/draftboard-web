/*
 * FIXME: this file needs to be refactored. component state can be decupled from
 * the component. we don't need ot change the composition just for if something is live or not.
 */

import React from 'react';
import ResultsHeader from './results-header.jsx';
import ResultsLineups from './results-lineups.jsx';
import ResultsStats from './results-stats.jsx';
import { isTimeInFuture } from '../../lib/utils';


/*
 * The overarching component for the results section.
 */
const ResultsStatic = (props) => {
  const { year, month, day, isWatchingLive, formattedDate } = props.date;

  let dayResults = props.results[formattedDate] || null;
  if (isWatchingLive === true) {
    dayResults = props.resultsWithLive || null;
  }


  let liveLineupsComponent = [];

  // Live lineups.
  if (props.currentLineups) {
    // currentLineups contains upcoming lineups. We don't want to show them on the results page
    // so let's strip out any lineups that haven't started yet.
    const liveLineups = props.currentLineups.filter((lineup) => !isTimeInFuture(lineup.start));

    liveLineupsComponent = (
      <ResultsLineups
        isWatchingLive
        lineups={liveLineups}
      />
    );
  }

  let statsAndLineups;
  let statsresults;
  if (dayResults !== null) {
    statsresults = (
      <ResultsStats stats={dayResults.overall} />
    );
    statsAndLineups = (
      <ResultsLineups
        isWatchingLive={isWatchingLive}
        lineups={dayResults.lineups}
        fetchContestResults={props.fetchContestResults}
      />
    );
  } else {
    // Show empty stats line to prevent rendering glitches.
    statsAndLineups = (
      <div key="past-lineups">
        <ResultsStats />
      </div>
    );
  }

  return (
    <div className="inner">
      <ResultsHeader
        year={year}
        month={month}
        day={day}
        isWatchingLive={isWatchingLive}
        onSelectDate={props.onSelectDate}
        watchLiveLineups={props.watchLiveLineups}
      />
      <div className="results-page--data">
        {statsresults}
        {statsAndLineups}
        {liveLineupsComponent}
      </div>
    </div>
  );
};

ResultsStatic.propTypes = {
  params: React.PropTypes.object,
  results: React.PropTypes.object.isRequired,
  date: React.PropTypes.shape({
    year: React.PropTypes.number,
    month: React.PropTypes.number,
    day: React.PropTypes.number,
    isWatchingLive: React.PropTypes.boolean,
    formattedDate: React.PropTypes.string,
  }),
  onSelectDate: React.PropTypes.func.isRequired,
  resultsWithLive: React.PropTypes.object.isRequired,
  watchLiveLineups: React.PropTypes.func,
  fetchContestResults: React.PropTypes.func.isRequired,
  draftGroupInfo: React.PropTypes.object,
  currentLineups: React.PropTypes.array,
};

export default ResultsStatic;
