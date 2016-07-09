import GameTime from '../site/game-time';
import PureRenderMixin from 'react-addons-pure-render-mixin';
import React from 'react';


/**
 * Responsible for rendering a singe contest game item.
 */
const NavScoreboardGame = React.createClass({

  propTypes: {
    game: React.PropTypes.object.isRequired,
  },

  mixins: [PureRenderMixin],

  renderClock() {
    const { game } = this.props;
    const { boxscore = {}, sport, start, status } = game;

    const gameTimeProps = {
      boxscore,
      modifiers: ['nav-scoreboard'],
      sport,
      start,
      status,
    };

    return (<GameTime {...gameTimeProps} />);
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

        {this.renderClock()}
      </div>
    );
  },
});


export default NavScoreboardGame;
