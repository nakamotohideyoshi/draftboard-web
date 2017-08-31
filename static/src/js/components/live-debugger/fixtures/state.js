import { merge } from 'lodash';

const stubMyLineup = {
  id: 2,
  name: 'My Lineup',
  fp: 50,
  isLoading: false,
  potentialWinnings: 10,
  rank: 5,
  timeRemaining: {
    decimal: 0.91,
    duration: 50,
  },
};

const stubOppLineup = {
  id: 3,
  name: 'Opponent Lineup',
  fp: 20,
  potentialWinnings: 10,
  rank: '',
  timeRemaining: {
    decimal: 0.91,
    duration: 50,
  },
  isLoading: false,
};

const stubOtherLineup = {
  id: 4,
  name: 'Other Lineup',
  fp: 15,
  potentialWinnings: 10,
  rank: '',
  timeRemaining: {
    decimal: 0.91,
    duration: 50,
  },
  isLoading: false,
};

const stubDebugLineup = {
  id: 5,
  name: 'Debug Lineup',
  fp: 34,
  potentialWinnings: 10,
  rank: '',
  timeRemaining: {
    decimal: 0.91,
    duration: 50,
  },
  isLoading: false,
};

const stubContest = {
  id: 1,
  name: 'Debug Contest',
  potentialWinnings: 10,
  rank: 2,
  isLoading: false,
  hasLineupsUsernames: true,
  lineups: {
    [stubMyLineup.id]: merge(stubMyLineup, { rank: 1, potentialWinnings: 100 }),
    [stubOppLineup.id]: merge(stubOppLineup, { rank: 3, potentialWinnings: 50 }),
    [stubOtherLineup.id]: merge(stubOtherLineup, { rank: 3 }),
    [stubDebugLineup.id]: merge(stubDebugLineup, { rank: 4 }),
  },
  lineupsUsernames: {
    [stubMyLineup.id]: stubMyLineup.name,
    [stubOppLineup.id]: stubOppLineup.name,
    [stubOtherLineup.id]: stubOtherLineup.name,
    [stubDebugLineup.id]: stubDebugLineup.name,
  },
  rankedLineups: [
    stubMyLineup.id,
    stubOppLineup.id,
    stubOtherLineup.id,
    stubDebugLineup.id,
  ],
  prize: {
    info: {
      buyin: 1,
      payout_spots: 3,
      pk: 0,
      prize_pool: 0,
      ranks: [{
        category: 'cash',
        rank: 1,
        value: 1.8,
      }],
    },
  },
};

const stubAvailableLineups = [stubMyLineup, stubOppLineup, stubOtherLineup, stubDebugLineup];

export default {
  watching: {
    sport: 'nfl', // nba
    contestId: null,
    myLineupId: stubMyLineup.id,
    opponentLineupId: 4, // Null if you don't want to see the opponents overall-stats
  },
  currentEvent: null,
  eventsMultipart: {},
  contest: stubContest,
  uniqueLineups: {
    lineups: stubAvailableLineups,
  },
  myLineupInfo: stubMyLineup,
  opponentLineup: stubOppLineup,
  selectLineup: () => { },
};
