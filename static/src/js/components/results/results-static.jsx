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
        fetchEntryResults={props.fetchEntryResults}
      />
    );
  }

  let statsAndLineups;
  if (dayResults !== null) {
    statsAndLineups = (
      <div key="past-lineups">
        <ResultsStats stats={dayResults.overall} />
        <div className="results-page--data">
          <ResultsLineups
            isWatchingLive={isWatchingLive}
            lineups={dayResults.lineups}
            fetchEntryResults={props.fetchEntryResults}
          />
        </div>
      </div>
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

      {statsAndLineups}

      <div key="live-lineups">
        <h3>Live Lineups</h3>
        <div className="results-page--lineups">
          {liveLineupsComponent}
        </div>
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
  fetchEntryResults: React.PropTypes.func.isRequired,
  draftGroupInfo: React.PropTypes.object,
  currentLineups: React.PropTypes.array,
};

export default ResultsStatic;
