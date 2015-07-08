'use strict';

var React = require('react');


var ContestNavFilters = React.createClass({

  getInitialState: function() {
    return {};
  },

  render: function() {
    return (
      <div className="cmp-contest-nav--filters">
        <div className="cmp-contest-nav--sport-nav select-list">
          <div className="select-list--selected">NBA</div>

          <ul className="select-list--options">
            <li>NBA</li>
            <li>MLB</li>
            <li>NFL</li>
          </ul>
        </div>

        <div className="cmp-contest-nav--team-nav select-list">
          <div className="select-list--selected">Warriors Stack Team</div>

          <ul className="select-list--options">
            <li>Warriors Stack Team</li>
            <li>Nuggets Stack Team</li>
            <li>Fire Fire Fire!! </li>
          </ul>
        </div>
      </div>
    );
  }

});


module.exports = ContestNavFilters;
