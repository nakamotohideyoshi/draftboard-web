import React from 'react';
import PureRenderMixin from 'react-addons-pure-render-mixin';
import moment from 'moment';

/**
 * Responsible for rendering a singe contest game item.
 */
const NavScoreboardGame = React.createClass({

  propTypes: {
    game: React.PropTypes.object.isRequired,
  },

  mixins: [PureRenderMixin],

  renderClock() {
    const game = this.props.game;

    // if the game hasn't started
    if (game.hasOwnProperty('boxscore') && game.boxscore.quarter !== '') {
      const boxScore = game.boxscore;

      // if the game has ended
      if (boxScore.status === 'closed') {
        return (
          <div className="right">
            Final
          </div>
        );
      }

      // otherwise the game is live
      let clock = boxScore.clock;
      if (clock === '00:00') {
        clock = 'END OF';
      }

      return (
        <div className="right">
          { clock }
          <br />
          { boxScore.quarterDisplay }
        </div>
      );
    }

    return (
      <div className="right">
        { moment(game.start).format('h:mma') } <br /> <br />
      </div>
    );
  },

  renderScores() {
    const game = this.props.game;

    // if the game hasn't started
    if (game.hasOwnProperty('boxscore') && game.boxscore.quarter !== '') {
      const boxScore = game.boxscore;

      return (
        <div className="scores">
          { boxScore.away_score }
          <br />
          { boxScore.home_score }
        </div>
      );
    }

    return null;
  },

  render() {
    const game = this.props.game;

    return (
      <div className="game scroll-item game--is-live">
        <div className="left">
          {game.awayTeamInfo.alias}
          <br />
          {game.homeTeamInfo.alias}
        </div>

        { this.renderScores() }
        { this.renderClock() }
      </div>
    );
  },
});


export default NavScoreboardGame;
