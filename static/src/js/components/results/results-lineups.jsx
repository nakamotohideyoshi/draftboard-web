import React from 'react';
import extend from 'lodash/extend';
import ResultsLineup from './results-lineup.jsx';


const ResultsLineups = (props) => {
  if (props.lineups.length === 0) {
    return (
      <div>No contests entered on this date.</div>
    );
  }

  return (
    <div className="results-page--lineups">
      {props.lineups.map((lineup) => React.createElement(
        ResultsLineup, extend(
          {}, lineup, { key: lineup.id, dateIsToday: props.dateIsToday }
        ))
      )}
    </div>
  );
};

ResultsLineups.propTypes = {
  dateIsToday: React.PropTypes.bool.isRequired,
  lineups: React.PropTypes.array.isRequired,
};

export default ResultsLineups;
