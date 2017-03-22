import mockStore from '../mock-store-with-middleware';
import merge from 'lodash/merge';
import proxyquire from 'proxyquire';
import { assert } from 'chai';

import * as actions from '../../actions/events';
import * as types from '../../action-types';
import currentLineupsReducer from '../../reducers/current-lineups';
import eventsReducer from '../../reducers/events';
import liveDraftGroupsReducer from '../../reducers/live-draft-groups';
import sportsReducer from '../../reducers/sports';
import watchingReducer from '../../reducers/watching';


const event = {
  message: {
    at_bat: {
      srid_hitter: 'player4',
      srid_team: 'team1',
    },
    pbp: {
      flags: {
        is_ab_over: false,
      },
      id: 'pbp1',
      srid_at_bat: 'atbat1',
      srid_game: 'game1',
      srid_pitcher: 'player1',
    },
  },
  sport: 'mlb',
  type: 'pbp',
};
const gameId = '73e40c5f-c690-4936-8853-339ed43dcc76';

describe('actions.events.addEventAndStartQueue', () => {
  // initial state to mock the store with
  const defaultEventStore = {
    events: eventsReducer(undefined, {}),
    sports: sportsReducer(undefined, {}),
  };

  it('should correctly add pbp event and start up queue', () => {
    const defaultMessage = {
      at_bat: {
        srid_hitter: 'player4',
        srid_team: 'team1',
      },
      pbp: {
        flags: {
          is_ab_over: false,
        },
        id: 'pbp1',
        srid_at_bat: 'atbat1',
        srid_game: 'game1',  // in state.sports.games
        srid_pitcher: 'player1',
      },
    };

    // initial store, state
    const store = mockStore(defaultEventStore);

    // data coming out
    const expectedActions = [{
      type: types.EVENT_GAME_QUEUE_PUSH,
      event,
    }];

    return store.dispatch(actions.addEventAndStartQueue(gameId, defaultMessage, 'pbp', 'mlb'))
      .then(() => {
        assert.deepEqual(store.getActions(), expectedActions);
      });
  });
});

describe('actions.events.showGameEvent', () => {
  // initial state to mock the store with
  const defaultStore = {
    currentLineups: currentLineupsReducer(undefined, {}),
    events: eventsReducer(undefined, {}),
    liveDraftGroups: liveDraftGroupsReducer(undefined, {}),
    sports: sportsReducer(undefined, {}),
    watching: watchingReducer(undefined, {}),
  };

  // update with game data, for big plays
  defaultStore.sports.games = {
    '73e40c5f-c690-4936-8853-339ed43dcc76': {
      home_score: 3,
      away_score: 2,
      sport: 'mlb',
      srid_home: 'c69073e40c5f-4936-8853-339ed43dcc76',
      srid_away: '339ed43dcc76-c69073e40c5f-4936-8853',
    },
  };
  defaultStore.sports.mlb.teams = {
    'c69073e40c5f-4936-8853-339ed43dcc76': {
      alias: 'Team1',
    },
    '339ed43dcc76-c69073e40c5f-4936-8853': {
      alias: 'Team2',
    },
  };

  defaultStore.sports.nba.gameIds = [gameId];

  const defaultMessage = {
    description: '',
    eventPlayers: ['player1', 'player4'],
    gameId,
    hitter: {
      name: ' ',
      sridPlayer: 'player4',
      sridTeam: 'team1',
      outcomeFp: 0,
    },
    id: 'pbp1',
    isAtBatOver: false,
    pitchCount: '0B/0S - 0 Outs',
    runnerIds: [],
    runners: [],
    playersStats: {},
    sport: 'mlb',
    sridAtBat: 'atbat1',
    when: { half: false, inning: false, humanized: false },
    zonePitches: [],
  };

  it('should create promise of multievent and updating stats if valid mlb pbp with relevant player', () => {
    // use proxyquire to mock in responses
    const proxyActions = proxyquire('../../actions/events', {
      '../selectors/watching': {
        watchingOpponentLineupSelector: ({}) => ({
          isLoading: false,
          rosterBySRID: ['player1'],  // matches player in message!
        }),
        relevantGamesPlayersSelector: ({}) => ({ relevantItems: { players: ['player1'] } }),
      },
    });

    // initial store, state
    const store = mockStore(defaultStore);

    // data coming out
    const expectedActions = [{
      type: 'BATCHING_REDUCER.BATCH',
      payload: [
        {
          type: types.EVENT_MULTIPART_SET,
          key: 'atbat1',
          value: merge({}, defaultMessage, {
            awayScoreStr: 'Team2 2',
            homeScoreStr: 'Team1 3',
            relevantPlayersInEvent: ['player1'],
            whichSide: 'mine',
            winning: 'home',
            playerNames: {},
          }),
        },
        {
          type: types.EVENT_MULTIPART_MERGE_PLAYERS,
          players: ['player1'],
          eventId: 'atbat1',
        },
      ],
    }];

    return store.dispatch(proxyActions.showGameEvent(defaultMessage))
      .then(() => assert.deepEqual(store.getActions(), expectedActions));
  });
});
