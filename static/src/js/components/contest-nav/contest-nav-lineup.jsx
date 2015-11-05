'use strict';

const React = require('react');
const PureRenderMixin = require('react-addons-pure-render-mixin');


/**
 * Responsible for rendering a singe lineup item.
 */
const ContestNavLineup = React.createClass({

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

  render() {
    const {name, contest, time, pmr, points, balance} = this.props.lineup;

    return (
      <div className="lineup">
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


module.exports = ContestNavLineup;
