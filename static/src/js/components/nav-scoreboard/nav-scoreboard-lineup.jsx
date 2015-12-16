'use strict';

import React from 'react';
import PureRenderMixin from 'react-addons-pure-render-mixin';


/**
 * Responsible for rendering a singe lineup item.
 */
const NavScoreboardLineup = React.createClass({

  mixins: [PureRenderMixin],

  propTypes: {
    // Example:
    //
    // id      -> 1
    // name    -> 'Currys Chicken'
    // contest -> 'NBA'
    // time    -> '7:10PM'
    // pmr     -> 42
    // points  -> 89
    // balance -> '20$'
    //
    lineup: React.PropTypes.object.isRequired
  },

  openLineup() {
    window.location.pathname = '/live/lineups/' + this.props.lineup.id.toString()
  },

  render() {
    const {contest, time, pmr, points, balance} = this.props.lineup;
    let { name } = this.props.lineup

    if (name === '') {
      name = 'Currys Chicken'
    }

    return (
      <div className="lineup" onClick={ this.openLineup }>
        <div className="left">
          <span className="header">
            {contest} - {time}
          </span>
          <br />
          {name}
        </div>

        <div className="right">
          {points} <span className="unit">PTS / </span>
          {pmr} <span className="unit">PMR / </span>
          <span className="balance">{balance}</span>
        </div>
      </div>
    );
  }

});


export default NavScoreboardLineup;
