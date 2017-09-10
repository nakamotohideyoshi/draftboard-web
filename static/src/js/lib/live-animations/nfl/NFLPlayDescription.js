import { get } from 'lodash';
import NFLPlayRecapVO from './NFLPlayRecapVO';

/**
 * Formats the provided yards into a string.
 */
const formatYards = yards => {
  const suffix = yards === 0 || yards > 1 ? 's' : '';
  return `${Math.floor(yards)} yard${suffix}`;
};

/**
 * Creates a token representing an NFL player.
 */
const createPlayerToken = (recap, srid) => {
  const players = recap._obj.players.filter(player => srid === player.srid_player);
  let text = 'Unknown Player';
  let lineup = 'none';

  if (players.length >= 1) {
    text = `${players[0].first_name} ${players[0].last_name}`;
    lineup = 'todo';
  }

  return { type: 'player', text, lineup };
};

/**
 * Creates a token representing a string.
 */
const createStringToken = (text) => (
  { type: 'string', text }
);

/**
 * Returns the recap as a tokenized description.
 */
const tokenizeDescription = recap => {
  const endMarket = get(recap._obj, 'pbp.end_situation.location.alias', '???');
  const endYardline = get(recap._obj, 'pbp.end_situation.location.yardline', 99);

  let tokens = [recap._obj.pbp.description];

  /* eslint-disable max-len */

  if (recap.playType() === NFLPlayRecapVO.PASS) {
    const qb = createPlayerToken(recap, get(recap._obj, 'pbp.statistics.pass__list.player'));
    const receiver = createPlayerToken(recap, get(recap._obj, 'pbp.statistics.receive__list.player'));
    const completedYards = Math.floor((recap.passingYards() + recap.rushingYards()) * 100);
    const attemptedYards = get(recap._obj, 'pbp.statistics.pass__list.att_yards', '404');
    const isUnknownReceiver = receiver.text === 'Unknown Player';

    if (recap.isTurnover() && isUnknownReceiver) {
      tokens = [qb, 'pass intercepted!'];
    } else if (recap.isTurnover()) {
      tokens = [qb, 'pass intercepted! Intended for', receiver, '.'];
    } if (recap.isTouchdown()) {
      tokens = [qb, 'to', receiver, `for ${formatYards(completedYards)} and the touchdown!`];
    } else if (recap.isIncompletePass() && isUnknownReceiver) {
      tokens = [qb, `${attemptedYards} yard pass incomplete.`];
    } else if (recap.isIncompletePass()) {
      tokens = [qb, `${attemptedYards} yard pass incomplete. Intended for`, receiver, '.'];
    } else {
      tokens = [qb, 'to', receiver, `for ${formatYards(completedYards)} to the ${endMarket} ${endYardline}.`];
    }
  }

  if (recap.playType() === NFLPlayRecapVO.RUSH) {
    const rusher = createPlayerToken(recap, get(recap._obj, 'pbp.statistics.rush__list.player'));
    const rushingYards = Math.floor(recap.rushingYards() * 100);

    if (recap.isTouchdown()) {
      tokens = [rusher, `rushed ${recap.side()} for ${formatYards(rushingYards)} and the touchdown!`];
    } else if (endYardline === 50) {
      tokens = [rusher, `rushed ${recap.side()} for ${formatYards(rushingYards)} to the ${endYardline}.`];
    } else {
      tokens = [rusher, `rushed ${recap.side()} for ${formatYards(rushingYards)} to the ${endMarket} ${endYardline}.`];
    }
  }

  if (recap.playType() === NFLPlayRecapVO.PUNT) {
    const receiver = createPlayerToken(recap, get(recap._obj, 'pbp.statistics.return__list.player'));
    const kickingTeam = get(recap._obj, 'pbp.start_situation.possession.alias', '???');
    const returnYards = recap.rushingYards() * 100;

    if (recap.isTouchdown()) {
      tokens = [receiver, `returns the ${kickingTeam} punt ${formatYards(returnYards)} for touchdown!`];
    } else if (endYardline === 50) {
      tokens = [receiver, `returns the ${kickingTeam} punt ${formatYards(returnYards)} to the ${endYardline}.`];
    } else {
      tokens = [receiver, `returns the ${kickingTeam} punt ${formatYards(returnYards)} to the ${endMarket} ${endYardline}.`];
    }
  }

  if (recap.playType() === NFLPlayRecapVO.KICKOFF) {
    const receiver = createPlayerToken(recap, get(recap._obj, 'pbp.statistics.return__list.player'));
    const kickingTeam = get(recap._obj, 'pbp.start_situation.possession.alias', '???');
    const returnYards = get(recap._obj, 'pbp.statistics.return__list.yards', 0);

    if (recap.isTouchdown()) {
      tokens = [receiver, `returns the ${kickingTeam} kick ${formatYards(returnYards)} for touchdown!`];
    } else if (endYardline === 50) {
      tokens = [receiver, `returns the ${kickingTeam} kick ${formatYards(returnYards)} to the ${endYardline}.`];
    } else {
      tokens = [receiver, `returns the ${kickingTeam} kick ${formatYards(returnYards)} to the ${endMarket} ${endYardline}.`];
    }
  }

  if (recap.isQBSack()) {
    const qb = createPlayerToken(recap, get(recap._obj, 'pbp.statistics.pass__list.player'));
    const loss = Math.abs(get(recap._obj, 'pbp.statistics.pass__list.sack_yards', 99));

    if (endYardline === 50) {
      tokens = [qb, `sacked at the 50 for a loss of ${loss}.`];
    } else {
      tokens = [qb, `sacked at the ${endMarket} ${endYardline} for a loss of ${loss}.`];
    }
  }

  if (recap.isFumble()) {
    tokens.push([`Fumble! Recovered by ${endMarket}.`]);
  }

  if (recap.isSafety()) {
    tokens.push(['Safety!']);
  }

  /* eslint-enable max-len */

  return tokens.map(token => (
    token.hasOwnProperty('text') ? token : createStringToken(token)
  ));
};

export default class NFLPlayDescription {

  constructor(recap) {
    this._tokens = tokenizeDescription(recap);
  }

  /**
   * Returns the description as an HTML string.
   */
  toHTML() {
    return this._tokens.reduce((str, token) => {
      if (token.hasOwnProperty('type') && token.type === 'player') {
        return `${str} <span class="${token.lineup}"">${token.text}</span>`;
      }
      return `${str} ${token.text}`;
    }, '');
  }

  /**
   * Returns the description as a plain string.
   */
  toText() {
    return this._tokens.reduce((str, token) => `${str} ${token.text}`, '');
  }
}
