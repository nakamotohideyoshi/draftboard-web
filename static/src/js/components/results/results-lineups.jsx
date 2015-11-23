'use strict';

import React from 'react';
import { extend } from 'lodash';
import ResultsLineup from './results-lineup.jsx';


const ResultsLineups = React.createClass({

  propTypes: {
    lineups: React.PropTypes.array.isRequired
  },

  render() {
    return (
      <div className="results-page--lineups">
        {this.props.lineups.map((lineup) => {
          return React.createElement(ResultsLineup, extend(
            {}, lineup, {key: lineup.id}
          ));
        })}
      </div>
    );
  }

});


export default ResultsLineups;
