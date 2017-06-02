const stubMyLineup = {
  id: 2,
  name: 'My Lineup',
  fp: 5,
  isLoading: false,
  potentialWinnings: 10,
  rank: 1,
  timeRemaining: {
    decimal: 0.91,
    duration: 50,
  },
};

const stubOppLineup = {
  id: 3,
  name: 'Opponent Lineup',
  fp: 20,
  rank: 2,
  potentialWinnings: 10,
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
  rank: 3,
  potentialWinnings: 10,
  timeRemaining: {
    decimal: 0.91,
    duration: 50,
  },
  isLoading: false,
};

const stubDebugLineup = {
  id: 5,
  name: 'Debug Lineup',
  fp: 50,
  rank: 4,
  potentialWinnings: 10,
  timeRemaining: {
    decimal: 0.91,
    duration: 50,
  },
  isLoading: false,
};

const stubContest = {
  name: 'Debug Contest',
  potentialWinnings: 10,
  rank: 2,
  isLoading: false,
  hasLineupsUsernames: true,
  lineups: {
    [stubMyLineup.id]: stubMyLineup,
    [stubOppLineup.id]: stubOppLineup,
    [stubOtherLineup.id]: stubOtherLineup,
    [stubDebugLineup.id]: stubDebugLineup,
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
    contestId: 2,
    myLineupId: stubMyLineup.id,
    opponentLineupId: 3, // Null if you don't want to see the opponents overall-stats
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
