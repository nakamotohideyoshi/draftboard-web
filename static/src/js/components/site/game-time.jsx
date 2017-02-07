import moment from 'moment';
import React from 'react';
import { generateBlockNameWithModifiers } from '../../lib/utils/bem';
import { hasGameStarted } from '../../actions/sports';
import { stringifyMLBWhen } from '../../actions/events/pbp';
import { trackUnexpected } from '../../actions/track-exceptions';
import log from '../../lib/logging';

// assets
if (process.env.NODE_ENV !== 'test') {
  require('../../../sass/blocks/site/game-time.scss');
}


/**
 * Stateless component that houses the time of a game, be it inning+half for MLB, or clock + period for NHL, NFL, NBA
 *
 * @param  {object} props React props
 * @return {jsx}          JSX of component
 */
const GameTime = (props) => {
  const { modifiers, game } = props;
  const { boxscore, sport, start, status } = game;
  const block = 'game-time';

  const hasNotStarted = !hasGameStarted(sport, game);
  let value = null;

  // always have sport modifier
  modifiers.push(sport);

  // if game hasn't started
  if (hasNotStarted) {
    modifiers.push('has-not-started');
    value = moment(start).format('h:mma');

  // if game has ended
  } else if (['closed', 'complete'].indexOf(status) !== -1) {
    modifiers.push('game-complete');
    value = 'Final';

  // otherwise it's live
  } else {
    modifiers.push('is-live');

    switch (sport) {
      case 'mlb': {
        if (!('inning' in boxscore) || !('inning_half' in boxscore)) {
          modifiers.push('has-not-started');
          value = moment(start).format('h:mma');

          // this shouldn't happen
          trackUnexpected('<GameTime /> in live MLB but no (half) inning', { props });
          break;
        }

        const inning = stringifyMLBWhen(boxscore.inning);
        const inningHalf = boxscore.inning_half.toLowerCase();  // TODO change this to camelcase in store

        value = (
          <div>
            <svg
              className={`${block}__half-inning ${block}__half-inning--${(inningHalf)}`}
              viewBox="0 0 40 22.12"
            >
              <path d="M20,31.06L0,8.94H40Z" transform="translate(0 -8.94)" />
            </svg>
            <div className={`${block}__inning`}>
              {inning}
            </div>
          </div>
        );
        break;
      }

      case 'nba':
      case 'nhl':
      case 'nfl': {
        if (!('clock' in boxscore) || !('periodDisplay' in boxscore)) {
          modifiers.push('has-not-started');
          value = moment(start).format('h:mma');

          // this shouldn't happen
          log.warn('<GameTime /> in live but no clock|periodDisplay', { props });
          break;
        }

        const clock = (boxscore.clock === '00:00') ? 'END OF' : boxscore.clock;  // TODO switch this to within action
        value = (
          <div>
            <div className={`${block}__clock`}>{clock}</div>
            <div className={`${block}__period`}>{boxscore.periodDisplay}</div>
          </div>
        );

        break;
      }

      default:
        break;
    }
  }


  const classNames = generateBlockNameWithModifiers(block, modifiers);

  return (<div className={classNames}>{value}</div>);
};

GameTime.propTypes = {
  game: React.PropTypes.object,
  modifiers: React.PropTypes.array,
};

GameTime.defaultProps = {
  game: {
    boxscore: {
      clock: null,
      inning: null,
      inning_half: null,
      periodDisplay: null,
      quarter: null,
    },
  },
  modifiers: [],
};

export default GameTime;
