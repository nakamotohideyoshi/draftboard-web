import ActionTypes from '../action-types'
import {merge as _merge, find as _find, forEach as _forEach} from 'lodash'


const initialState = {
  errorMessage: null,
  lineupTitle: null,
  lineup: [],
  remainingSalary: 0,
  avgRemainingPlayerSalary: 0,
  contestSalaryLimit: 0,
  availablePositions: []
}

// Roster templates for empty lineup cards.
const rosterTemplates = {
  'nfl': [
    {idx: 0, name: 'QB', positions: ['QB'], player: null},
    {idx: 1, name: 'RB', positions: ['RB', 'FB'], player: null},
    {idx: 2, name: 'RB', positions: ['RB', 'FB'], player: null},
    {idx: 3, name: 'WR', positions: ['WR'], player: null},
    {idx: 4, name: 'WR', positions: ['WR'], player: null},
    {idx: 5, name: 'TE', positions: ['TE'], player: null},
    {idx: 6, name: 'FX', positions: ['RB','FB','WR','TE'], player: null},
    {idx: 7, name: 'FX', positions: ['RB','FB','WR','TE'], player: null}
  ],
  'nba': [
    {idx: 0, name: 'G', positions: ['PG', 'SG'], player: null},
    {idx: 1, name: 'G', positions: ['PG', 'SG'], player: null},
    {idx: 2, name: 'F', positions: ['SF', 'PF'], player: null},
    {idx: 3, name: 'F', positions: ['SF', 'PF'], player: null},
    {idx: 4, name: 'C', positions: ['C'], player: null},
    {idx: 5, name: 'FX', positions: ['PG','SG','SF','PF','C'], player: null},
    {idx: 6, name: 'FX', positions: ['PG','SG','SF','PF','C'], player: null},
    {idx: 7, name: 'FX', positions: ['PG','SG','SF','PF','C'], player: null}
  ],
  'nhl': [
    {idx: 0, name: 'F', positions: ['C', 'LW', 'RW'], player: null},
    {idx: 1, name: 'F', positions: ['C', 'LW', 'RW'], player: null},
    {idx: 2, name: 'F', positions: ['C', 'LW', 'RW'], player: null},
    {idx: 3, name: 'D', positions: ['D'], player: null},
    {idx: 4, name: 'D', positions: ['D'], player: null},
    {idx: 5, name: 'FX', positions: ['C','D','LW','RW'], player: null},
    {idx: 6, name: 'FX', positions: ['C','D','LW','RW'], player: null},
    {idx: 7, name: 'G', positions: ['G'], player: null}
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

const salaryCaps = {
  'nba': 50000,
  'nfl': 50000,
  'nhl': 50000,
  'mlb': 50000
};


const getAvailableLineupSlots = function(state) {
  return state.lineup.filter(function(slot) {
    if(!slot.player) {
      return slot;
    }
  })
}


/**
 * Insert the provided player into the lineup. This will place the player in the next avialable
 * slot that is valid for the player's position. NOTE: You should use addPlayer(), not this.
 * @param  {Object} player A row from the DraftGroupStore.
 */
const insertPlayerIntoLineup = function(player, state) {
  var openSlots = getAvailableLineupSlots(state)

  for (var i=0; i < openSlots.length; i++) {
    if (openSlots[i].positions.indexOf(player.position) !== -1) {
      openSlots[i].player = player
      return state.lineup
    }
  }

  return state.lineup
}


/**
 * How many players have been added to the lineup.
 * @return {Integer} The number of players in the lineup.
 */
// const getPlayerCount = function(state) {
//   return state.lineup.reduce(function(prev, curr, i, lineup) {
//       if (lineup[i].player) {
//         return prev + 1;
//       }
//       return prev;
//   }, 0);
// }


/**
 * Get the sum of lineup players' salary.
 * @return {Integer} The total lineup salary.
 */
const getTotalSalary = function(state) {
  return state.lineup.reduce(function(previousValue, currentValue, index, lineup) {
    if (lineup[index].player) {
      return previousValue + lineup[index].player.salary;
    }
    // If there aren't any players in the lineup, return the default (0).
    return previousValue;
  }, 0);
}


/**
 * Find how much money is left to spend on players.
 * @return {Integer} Salary cap minus current lineup salary.
 */
const getRemainingSalary = function(state) {
  return state.contestSalaryLimit - getTotalSalary(state);
}


/**
 * Find the average remaining salary per available slots.
 * @return {Inteter} The average player salary, rounded down to the nearest Int.
 */
const getAvgRemainingPlayerSalary = function(state) {
  var EmptySlotCount = getAvailableLineupSlots(state).length;
    if (EmptySlotCount > 0) {
    return Math.floor(getRemainingSalary(state) / EmptySlotCount);
  }

  return 0;
}


/**
 * Determine which position types are still available.
 * @return {array} The avaolaible positions ex: ['WR', 'QB', 'DST']
 */
const findAvailablePositions = function(state) {
  var openSlots = getAvailableLineupSlots(state);
  var availablePositions = [];

  openSlots.forEach(function(slot) {
    availablePositions = availablePositions.concat(slot.positions);
  });

  return availablePositions
}


/**
 * Check if the player is already in the lineup.
 * @param  {Object} player A player.
 * @return {Boolean}
 */
const isPlayerInLineup = function(player, state) {
  return typeof _find(state.lineup, 'player', player) !== 'undefined';
}


/**
 *   Run through each unoccupied slot and determine if any are able to accept this player's
 *   position type. At this point, We don't care which slot specifically is open for the player,
 *   just that there is one.
 * @return {Boolean}
 */
const isSlotAvailableForPlayer = function(player, state) {
  var openSlots = getAvailableLineupSlots(state);

  // Once we find an open slot, return true;
  for (var i=0; i < openSlots.length; i++) {
    if (openSlots[i].positions.indexOf(player.position) !== -1) {
      return true;
    }
  }

  return false;
}


/**
 * Determine if we are able to add the supplied player to the lineup.
 * @param  {Object} player A player from the DraftGroupStore.
 * @return {bool}          Can the playe be added?
 */
const canAddPlayer = function(player, state) {
  // Check if the player is already in the lineup.
  if (isPlayerInLineup(player, state)) {
    console.error("Selected player is already in the lineup.")
    state.errorMessage = 'Selected player is already in the lineup'
    return false
  }

  // Check if there is room in the salary cap.
  // if (getTotalSalary(state) + player.salary > state.contestSalaryLimit) {
  //   console.error('Player exceeds maximum salary.')
  //   state.errorMessage = 'Player exceeds maximum salary'
  //   return false
  // }

  // Check if there is a valid slot for the player.
  if (!isSlotAvailableForPlayer(player, state)) {
    console.error("There is no slot available for this player.")
    state.errorMessage = 'There is no slot available for this player'
    return false
  }

  // If all checks pass, the player can be added.
  return true;
}


const addPlayer = function(player, state, callback) {
  let canAdd = canAddPlayer(player, state);

  if (canAdd) {
    let newLineup = insertPlayerIntoLineup(player, state)
    return callback(false, newLineup)
  } else {
    return callback(state.errorMessage, null)
  }
}


/**
 * Remove a player from the lineup.
 * @param  {int} playerId the player.player_id to remove.
 */
const removePlayer = function(playerId, state) {
  // Loop through each lineup slot looking for the specified player. once found, set the
  // player property to null.
  for (let slot of state.lineup) {
    if (slot.player) {
      if (playerId === slot.player.player_id) {
        slot.player = null;
        return;
      }
    }
  }
}




module.exports = function(state = initialState, action) {

  switch (action.type) {

    // Create an empty lineup card based on the roster of the sport of the current draftgroup.
    case ActionTypes.CREATE_LINEUP_INIT:
      // Return a copy of the previous state with our new things added to it.
      let newState = _merge({}, state, {
        lineup: rosterTemplates[action.sport],
        remainingSalary: salaryCaps[action.sport],
        contestSalaryLimit: salaryCaps[action.sport]
      })
      // After the state has a roster, find it's open positions.
      newState.availablePositions = findAvailablePositions(newState)
      newState.avgRemainingPlayerSalary = getAvgRemainingPlayerSalary(newState)
      return newState


    // Add provided player to the new lineup
    case ActionTypes.CREATE_LINEUP_ADD_PLAYER:
      // if there is an error adding the player, return the state with an error message
      return addPlayer(action.player, state, function(err, updatedLineup) {
        if (err) {
          return Object.assign({}, state, {
            errorMessage: err
          });
        }
        // If we can add the player, add them and update the state.
        else {
          _merge({}, state, {lineup: updatedLineup, errorMessage: null})
          let newState = _merge({}, state, {
            avgRemainingPlayerSalary:  getAvgRemainingPlayerSalary(state),
            remainingSalary: getRemainingSalary(state),
            errorMessage: null
          })
          // After the state's roster has been updated, find it's open positions.
          newState.availablePositions = findAvailablePositions(newState)
          return newState
        }
      });


    case ActionTypes.CREATE_LINEUP_REMOVE_PLAYER:
      newState = Object.assign({}, state, {
        errorMessage: null
      });
      removePlayer(action.playerId, newState)
      newState.avgRemainingPlayerSalary = getAvgRemainingPlayerSalary(newState)
      newState.remainingSalary = getRemainingSalary(newState)
      newState.availablePositions = findAvailablePositions(newState)
      return newState;


    case ActionTypes.CREATE_LINEUP_SAVE_FAIL:
      return Object.assign({}, state, {
        errorMessage: action.err
      });


    case ActionTypes.CREATE_LINEUP_IMPORT:
      newState = Object.assign({}, state);
      // We're passed a list of players. Make sure we're putting each one into the correct lineup
      // slot based on the idx property.
      _forEach(state.lineup, function(slot) {
        slot.player =  _find(action.players, 'idx', slot.idx)
      });

      // Update the title (optional)
      newState.lineupTitle = action.title
      return newState


    default:
      return state

  }
}
