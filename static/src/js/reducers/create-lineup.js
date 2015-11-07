import ActionTypes from '../action-types'

// Roster templates for empty lineup cards.
const rosterTemplates = {
  'nfl': [
    {idx: 0, name: 'QB', positions: ['QB'], player: null},
    {idx: 1, name: 'RB', positions: ['RB', 'FB'], player: null},
    {idx: 2, name: 'RB', positions: ['RB', 'FB'], player: null},
    {idx: 3, name: 'WR', positions: ['WR'], player: null},
    {idx: 4, name: 'WR', positions: ['WR'], player: null},
    {idx: 5, name: 'TE', positions: ['TE'], player: null},
    {idx: 6, name: 'FLEX', positions: ['RB','FB','WR','TE'], player: null},
    {idx: 7, name: 'FLEX', positions: ['RB','FB','WR','TE'], player: null},
    {idx: 8, name: 'DST', positions: ['DST'], player: null}
  ],
  'nba': [
    {idx: 0, name: 'PG', positions: ['PG'], player: null},
    {idx: 1, name: 'SG', positions: ['SG'], player: null},
    {idx: 2, name: 'SF', positions: ['SF'], player: null},
    {idx: 3, name: 'PF', positions: ['PF'], player: null},
    {idx: 4, name: 'C', positions: ['C'], player: null},
    {idx: 5, name: 'FLEX', positions: ['PG','SG','SF','PF','C'], player: null},
    {idx: 6, name: 'FLEX', positions: ['PG','SG','SF','PF','C'], player: null},
    {idx: 7, name: 'FLEX', positions: ['PG','SG','SF','PF','C'], player: null}
  ],
  'nhl': [
    {idx: 0, name: 'G', positions: ['G'], player: null},
    {idx: 1, name: 'C', positions: ['C'], player: null},
    {idx: 2, name: 'F', positions: ['LW', 'RW'], player: null},
    {idx: 3, name: 'F', positions: ['LW', 'RW'], player: null},
    {idx: 4, name: 'D', positions: ['D'], player: null},
    {idx: 5, name: 'D', positions: ['D'], player: null},
    {idx: 6, name: 'FLEX', positions: ['PG','SG','SF','PF','C'], player: null},
    {idx: 7, name: 'FLEX', positions: ['PG','SG','SF','PF','C'], player: null}
  ],
  'mlb': [
    {idx: 0, name: 'SP', positions: ['SP'], player: null},
    {idx: 1, name: 'SP', positions: ['SP'], player: null},
    {idx: 2, name: 'C', positions: ['C'], player: null},
    {idx: 3, name: '1B', positions: ['1B'], player: null},
    {idx: 4, name: '2B', positions: ['2B'], player: null},
    {idx: 5, name: '3B', positions: ['3B'], player: null},
    {idx: 6, name: 'SS', positions: ['SS'], player: null},
    {idx: 7, name: 'OF', positions: ['LF','CF','RF'], player: null},
    {idx: 8, name: 'OF', positions: ['LF','CF','RF'], player: null},
    {idx: 9, name: 'OF', positions: ['LF','CF','RF'], player: null}
  ]
}



module.exports = function(state = {}, action) {
  switch (action.type) {

    // Create an empty lineup card based on the roster of the sport of the current draftgroup.
    case ActionTypes.CREATE_LINEUP_INIT:
      // Return a copy of the previous state with our new things added to it.
      return Object.assign({}, state, {
        lineup: rosterTemplates[action.sport],
        remainingSalary: 666,
        avgPlayerSalary: 111,
        errorMessage: ''
      })


    default:
      return state

  }
}
