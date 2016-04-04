import React from 'react';
import { extend } from 'lodash';
import ResultsLineup from './results-lineup.jsx';


const ResultsLineups = React.createClass({

  propTypes: {
    dateIsToday: React.PropTypes.bool.isRequired,
    lineups: React.PropTypes.array.isRequired,
  },

  render() {
    if (this.props.lineups.length === 0) {
      return (
        <div>No contests entered on this date.</div>
      );
    }

    return (
      <div className="results-page--lineups">
        {this.props.lineups.map((lineup) => React.createElement(
          ResultsLineup, extend(
            {}, lineup, { key: lineup.id, dateIsToday: this.props.dateIsToday }
          ))
        )}
      </div>
    );
  },

});


export default ResultsLineups;
