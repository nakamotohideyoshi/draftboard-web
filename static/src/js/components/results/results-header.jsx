'use strict';

import React from 'react';

import {monthNumToName} from '../../lib/time.js';

const ResultsHeader = React.createClass({

  propTypes: {
    children: React.PropTypes.element
  },

  getTitle() {
    const today = new Date();

    return `Today, ${monthNumToName(today.getMonth())}
                   ${today.getDate()},
                   ${today.getFullYear()}`;
  },
  render() {
    return (
      <div className="results-page--header">
        <div className="title">
          <div className="text">Active & upcoming lineups</div>
          <div className="date">{this.getTitle()}</div>
        </div>

        {this.props.children}

        <div className="search">
          <div className="icon"></div>
        </div>
        <div className="draft-a-team">
          Draft a team
        </div>
      </div>
    );
  }

});


module.exports = ResultsHeader;
