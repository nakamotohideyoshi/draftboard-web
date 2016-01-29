import React from 'react';
import PureRenderMixin from 'react-addons-pure-render-mixin';


/**
 * Responsible for rendering a singe lineup item.
 */
const NavScoreboardLineup = React.createClass({

  propTypes: {
    lineup: React.PropTypes.object.isRequired,
  },

  mixins: [PureRenderMixin],

  openLineup() {
    window.location.pathname = `/live/lineups/${this.props.lineup.id.toString()}`
  },

  render() {
    const {
      contest,
      time,
      minutesRemaining,
      points,
      potentialEarnings,
    } = this.props.lineup;

    let { name } = this.props.lineup;

    if (name === '') {
      name = `Lineup for ${window.dfs.username}`
    }

    return (
      <div className="lineup" onClick={ this.openLineup }>
        <div className="left">
          <span className="header">
            { contest } - { time }
          </span>
          <br />
          { name }
        </div>

        <div className="right">
          { points } <span className="unit">PTS / </span>
          { minutesRemaining } <span className="unit">PMR / </span>
          <span className="balance">${ potentialEarnings }</span>
        </div>
      </div>
    );
  },
});


export default NavScoreboardLineup;
