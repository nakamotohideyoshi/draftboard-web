import { merge } from 'lodash';

const stubGenericLineupA = {
  id: 1,
  name: 'My Lineup',
  fp: 0,
  isLoading: false,
  potentialWinnings: 0,
  rank: 5,
  timeRemaining: {
    decimal: 0.91,
    duration: 50,
  },
};

const stubGenericLineupB = {
  id: 2,
  name: 'My Lineup',
  fp: 0,
  isLoading: false,
  potentialWinnings: 0,
  rank: 5,
  timeRemaining: {
    decimal: 0.91,
    duration: 50,
  },
};

const stubGenericLineupC = {
  id: 3,
  name: 'My Lineup',
  fp: 0,
  isLoading: false,
  potentialWinnings: 0,
  rank: 5,
  timeRemaining: {
    decimal: 0.91,
    duration: 50,
  },
};

const stubMyLineup = {
  id: 4,
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
  id: 5,
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
  id: 6,
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
  id: 7,
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
    [stubGenericLineupA.id]: merge(stubGenericLineupA, { fp: 0, rank: 7, potentialWinnings: 0 }),
    [stubGenericLineupB.id]: merge(stubGenericLineupB, { fp: 0, rank: 6, potentialWinnings: 0 }),
    [stubGenericLineupC.id]: merge(stubGenericLineupC, { fp: 0, rank: 5, potentialWinnings: 0 }),
    [stubMyLineup.id]: merge(stubMyLineup, { fp: 100, rank: 1, potentialWinnings: 100 }),
    [stubOppLineup.id]: merge(stubOppLineup, { fp: 50, rank: 2, potentialWinnings: 50 }),
    [stubOtherLineup.id]: merge(stubOtherLineup, { fp: 25, rank: 3, potentialWinnings: 50 }),
    [stubDebugLineup.id]: merge(stubDebugLineup, { fp: 25, rank: 4, potentialWinnings: 50 }),
  },
  lineupsUsernames: {
    [stubGenericLineupA.id]: stubGenericLineupA.name,
    [stubGenericLineupB.id]: stubGenericLineupB.name,
    [stubGenericLineupC.id]: stubGenericLineupC.name,
    [stubMyLineup.id]: stubMyLineup.name,
    [stubOppLineup.id]: stubOppLineup.name,
    [stubOtherLineup.id]: stubOtherLineup.name,
    [stubDebugLineup.id]: stubDebugLineup.name,
  },
  rankedLineups: [
    stubGenericLineupA.id,
    stubGenericLineupB.id,
    stubGenericLineupC.id,
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

export default {
  watching: {
    sport: 'nfl', // nba
    contestId: null,
    myLineupId: stubMyLineup.id,
    opponentLineupId: stubOppLineup.id, // Null if you don't want to see the opponents overall-stats
  },
  currentEvent: null,
  eventsMultipart: {},
  contest: stubContest,
  uniqueLineups: {
    lineups: stubContest.rankedLineups,
  },
  myLineupInfo: stubMyLineup,
  opponentLineup: stubOppLineup,
  selectLineup: () => { },
};
