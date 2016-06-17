import React from 'react';
import PureRenderMixin from 'react-addons-pure-render-mixin';
import moment from 'moment';
import { dateNow } from '../../lib/utils';
import { stringifyMLBWhen } from '../../actions/events-multipart';


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

    // default
    let clockElement = (<div>{moment(game.start).format('h:mma')} <br /> <br /></div>);

    const boxscore = game.boxscore || {};
    const hasGameStarted = boxscore.hasOwnProperty('status') &&
      boxscore.status !== 'scheduled' &&
      game.start < dateNow();

    // if the game hasn't started
    if (hasGameStarted) {
      // if the game has ended
      const doneStatuses = ['closed', 'complete'];
      if (doneStatuses.indexOf(boxscore.status) !== -1) {
        clockElement = 'Final';
      } else {
        switch (game.sport) {
          case 'mlb': {
            const strInning = stringifyMLBWhen(boxscore.inning, boxscore.innning_half);
            clockElement = (
              <div>
                <div className={`mlb-when mlb-half-inning--${(boxscore.inning_half === 'B') ? 'bottom' : 'top'}`}>
                  <svg className="down-arrow" viewBox="0 0 40 22.12">
                    <path d="M20,31.06L0,8.94H40Z" transform="translate(0 -8.94)" />
                  </svg>
                </div>
                {strInning}
              </div>
            );
            break;
          }
          case 'nba':
          case 'nhl':
          default: {
            // otherwise the game is live
            const clock = (boxscore.clock === '00:00') ? 'END OF' : boxscore.clock;
            clockElement = (<div>{clock}<br />{boxscore.periodDisplay}</div>);
          }
        }
      }
    }

    return (
      <div className="right">
        {clockElement}
      </div>
    );
  },

  renderInning() {

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
