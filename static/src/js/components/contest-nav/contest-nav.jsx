'use strict';

var React = require('react');
var ContestNavFilters = require('./contest-nav-filters.jsx');
var ContestNavContestList = require('./contest-nav-contest-list.jsx');
var renderComponent = require('../../lib/render-component');


var ContestNav = React.createClass({

  getInitialState: function() {
    // Fake contest data.
    return {
      contests: [
        {
          'id': 0,
          'title': '$150k NBA Championship',
          'winning': "$82",
          'position': '22',
          'entries': '1.8k'
        },
        {
          'id': 1,
          'title': '$150k NBA Championship',
          'winning': "$82",
          'position': '22',
          'entries': '1.8k'
        },
        {
          'id': 2,
          'title': '$150k NBA Championship',
          'winning': "$82",
          'position': '22',
          'entries': '1.8k'
        },
        {
          'id': 3,
          'title': '$150k NBA Championship',
          'winning': "$82",
          'position': '22',
          'entries': '1.8k'
        },
        {
          'id': 4,
          'title': '$150k NBA Championship',
          'winning': "$82",
          'position': '22',
          'entries': '1.8k'
        },
        {
          'id': 5,
          'title': '$150k NBA Championship',
          'winning': "$82",
          'position': '22',
          'entries': '1.8k'
        },
        {
          'id': 6,
          'title': '$150k NBA Championship',
          'winning': "$82",
          'position': '22',
          'entries': '1.8k'
        },
        {
          'id': 7,
          'title': '$150k NBA Championship',
          'winning': "$82",
          'position': '22',
          'entries': '1.8k'
        }
      ]
    };
  },

  render: function() {
    return (
      <div className="inner">
        <ContestNavFilters />
        <ContestNavContestList contests={this.state.contests} />
      </div>
    );
  }
});

renderComponent(<ContestNav />, '.cmp-contest-nav');

module.exports = ContestNav;
