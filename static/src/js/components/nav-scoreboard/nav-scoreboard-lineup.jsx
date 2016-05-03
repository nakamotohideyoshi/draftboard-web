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
    window.location.pathname = `/live/lineups/${this.props.lineup.id.toString()}`;
  },

  render() {
    const {
      formattedStart,
      timeRemaining,
      fp,
    } = this.props.lineup;

    const potentialWinnings = this.props.lineup.potentialWinnings || 0;
    const sport = this.props.lineup.sport;

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
          { fp } <span className="unit">PTS / </span>
          { timeRemaining.duration } <span className="unit">PMR / </span>
          <span className="balance">${ potentialWinnings.toFixed(2) }</span>
        </div>
      </div>
    );
  },
});


export default NavScoreboardLineup;
