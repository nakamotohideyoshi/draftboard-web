import GameTime from '../site/game-time';
import { isDateInTheFuture } from '../../lib/utils';
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

    const gameTimeProps = {
      game,
      modifiers: ['nav-scoreboard'],
    };

    return (<GameTime {...gameTimeProps} />);
  },

  renderScores() {
    const game = this.props.game;

    // if the game hasn't started
    if (game.hasOwnProperty('boxscore') &&
      game.boxscore.quarter !== '' &&
      !isDateInTheFuture(game.start)
    ) {
      return (
        <div className="scores">
          { game.away_score }
          <br />
          { game.home_score }
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
