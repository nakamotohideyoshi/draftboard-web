'use strict';

const React = require('react');

/**
 * Responsible for rendering a singe contest game item.
 */
const ContestNavGame = React.createClass({

  propTypes: {
    // Example game:
    //
    // id':      '0'
    // time':    '7:10PM'
    // players': ['ATL', 'BAL']
    //
    game: React.PropTypes.object.isRequired
  },

  render() {
    const {players, time} = this.props.game;

    return (
      <div className="game scroll-item">
        <div className="left">
          {players[0]}
          <br />
          {players[1]}
        </div>

        <div className="right">
          {time} <br /> <br />
        </div>
      </div>
    );
  }

});


module.exports = ContestNavGame;
