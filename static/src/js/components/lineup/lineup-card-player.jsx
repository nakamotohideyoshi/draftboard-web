'use strict';

var React = require('react');


var LineupCardPlayer = React.createClass({

  propTypes: {
    player: React.PropTypes.array
  },

  getDefaultProps: function(){
    // Since we don't have real data yet, add some empty lineups and let the LineupCard render whatever it likes.
    return {
      player: [

      ]
    };
  },

  // getInitialState: function() {
  //   return {};
  // },


  render: function() {
    return (
      <li className="cmp-lineup-card__player">
        <span className="cmp-lineup-card__position">PG</span>
        <span className="cmp-lineup-card__photo">😀</span>
        <span className="cmp-lineup-card__name">E. Mudiay</span>
        <span className="cmp-lineup-card__average">8</span>
      </li>
    );
  }
});


module.exports = LineupCardPlayer;
