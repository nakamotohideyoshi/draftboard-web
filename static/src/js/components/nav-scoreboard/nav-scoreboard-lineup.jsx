import React from 'react';
import PureRenderMixin from 'react-addons-pure-render-mixin';
import log from '../../lib/logging.js';


/**
 * Responsible for rendering a singe lineup item.
 */
const NavScoreboardLineup = React.createClass({

  propTypes: {
    lineup: React.PropTypes.object.isRequired,
  },

  mixins: [PureRenderMixin],

  openLineup() {
    window.location.pathname = `/live/lineups/${this.props.lineup.id.toString()}`;
  },

  render() {
    const {
      formattedStart,
      minutesRemaining,
      points,
      totalPotentialEarnings,
    } = this.props.lineup;

    log.warn(this.props.lineup);

    const sport = this.props.lineup.draftGroup.sport;

    let { name } = this.props.lineup;

    if (name === '') {
      name = `Lineup for ${window.dfs.username}`;
    }

    return (
      <div className="lineup" onClick={ this.openLineup }>
        <div className="left">
          <span className="header">
            { sport } - { formattedStart }
          </span>
          <br />
          <span className="name">{ name }</span>
        </div>

        <div className="right">
          { points } <span className="unit">PTS / </span>
          { minutesRemaining } <span className="unit">PMR / </span>
          <span className="balance">${ totalPotentialEarnings.toFixed(2) }</span>
        </div>
      </div>
    );
  },
});


export default NavScoreboardLineup;
