'use strict';

import React from 'react';
import PureRenderMixin from 'react-addons-pure-render-mixin';

/**
 * Responsible for rendering a singe contest game item.
 */
const NavScoreboardGame = React.createClass({

  mixins: [PureRenderMixin],

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


export default NavScoreboardGame;
