import React from 'react';
import ResultsHeader from './results-header.jsx';
import ResultsLineups from './results-lineups.jsx';
import ResultsStats from './results-stats.jsx';

/*
 * The overarching component for the results section.
 */
const ResultsStatic = (props) => {
  const { year, month, day, isWatchingLive, formattedDate } = props.date;

  let dayResults = props.results[formattedDate] || null;
  if (isWatchingLive === true) {
    dayResults = props.resultsWithLive || null;
  }

  let statsAndLineups;
  if (dayResults !== null) {
    statsAndLineups = (
      <div>
        <ResultsStats stats={dayResults.overall} />
        <ResultsLineups
          isWatchingLive={isWatchingLive}
          lineups={dayResults.lineups}
          fetchEntryResults={props.fetchEntryResults}
        />
      </div>
    );
  } else {
    // Show empty stats line to prevent rendering glitches.
    statsAndLineups = (
      <div>
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
      {statsAndLineups}
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
  fetchEntryResults: React.PropTypes.func.isRequired,
};

export default ResultsStatic;
