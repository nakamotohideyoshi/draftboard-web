import React from 'react';
import extend from 'lodash/extend';
import ResultsLineup from './results-lineup.jsx';


const ResultsLineups = (props) => {
  if (props.lineups.length === 0) {
    return (
      <div className="results-page__no-contests">No contests entered on this date.</div>
    );
  }

  return (
    <div className="results-page--lineups">
      {props.lineups.map((lineup) => React.createElement(
        ResultsLineup, extend(
          {},
          lineup,
          {
            key: lineup.id,
            isWatchingLive: props.isWatchingLive,
            fetchContestResults: props.fetchContestResults,
          }
        ))
      )}
    </div>
  );
};

ResultsLineups.propTypes = {
  isWatchingLive: React.PropTypes.bool,
  lineups: React.PropTypes.array.isRequired,
  fetchContestResults: React.PropTypes.func,
};

export default ResultsLineups;
