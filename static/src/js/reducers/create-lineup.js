import ActionTypes from '../action-types';
import merge from 'lodash/merge';
import find from 'lodash/find';
import forEach from 'lodash/forEach';
import log from '../lib/logging.js';
import { rosterTemplates, salaryCaps } from '../lib/lineup.js';
import { setInProgressLocalLineup } from '../lib/lineup-drafts';

const initialState = {
  errorMessage: null,
  lineupTitle: null,
  lineup: [],
  remainingSalary: 0,
  avgRemainingPlayerSalary: 0,
  contestSalaryLimit: 0,
  availablePositions: [],
  lineupCanBeSaved: false,
};


const getAvailableLineupSlots = (state) => state.lineup.filter((slot) => {
  if (!slot.player) {
    return slot;
  }

  return null;
});


/**
 * Insert the provided player into the lineup. This will place the player in the next avialable
 * slot that is valid for the player's position. NOTE: You should use addPlayer(), not this.
 * @param  {Object} player A row from the DraftGroupStore.
 */
const insertPlayerIntoLineup = (player, state) => {
  const openSlots = getAvailableLineupSlots(state);

  for (let i = 0; i < openSlots.length; i++) {
    if (openSlots[i].positions.indexOf(player.position) !== -1) {
      openSlots[i].player = player;
      return state.lineup;
    }
  }

  return state.lineup;
};


/**
 * How many players have been added to the lineup.
 * @return {Number} The number of players in the lineup.
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
 * @return {Number} The total lineup salary.
 */
const getTotalSalary = (state) => state.lineup.reduce((previousValue, currentValue, index, lineup) => {
  if (lineup[index].player) {
    return previousValue + lineup[index].player.salary;
  }
  // If there aren't any players in the lineup, return the default (0).
  return previousValue;
}, 0);


/**
 * Find how much money is left to spend on players.
 * @return {Number} Salary cap minus current lineup salary.
 */
const getRemainingSalary = (state) => state.contestSalaryLimit - getTotalSalary(state);


/**
 * Find the average remaining salary per available slots.
 * @return {Number} The average player salary, rounded down to the nearest Int.
 */
const getAvgRemainingPlayerSalary = (state) => {
  const EmptySlotCount = getAvailableLineupSlots(state).length;
  if (EmptySlotCount > 0) {
    return Math.floor(getRemainingSalary(state) / EmptySlotCount);
  }

  return 0;
};


/**
 * Determine which position types are still available.
 * @return {array} The avaolaible positions ex: ['WR', 'QB', 'DST']
 */
const findAvailablePositions = (state) => {
  const openSlots = getAvailableLineupSlots(state);
  let availablePositions = [];

  openSlots.forEach((slot) => {
    availablePositions = availablePositions.concat(slot.positions);
  });

  return availablePositions;
};


/**
 * Check if the player is already in the lineup.
 * @param  {Object} player A player.
 * @return {Boolean}
 */
const isPlayerInLineup = (player, state) => typeof find(
  state.lineup,
  (lineupPlayer) =>
    lineupPlayer.player && lineupPlayer.player.player_id === player.player_id
) !== 'undefined';


/**
 *   Run through each unoccupied slot and determine if any are able to accept this player's
 *   position type. At this point, We don't care which slot specifically is open for the player,
 *   just that there is one.
 * @return {Boolean}
 */
const isSlotAvailableForPlayer = (player, state) => {
  const openSlots = getAvailableLineupSlots(state);

  // Once we find an open slot, return true;
  for (let i = 0; i < openSlots.length; i++) {
    if (openSlots[i].positions.indexOf(player.position) !== -1) {
      return true;
    }
  }

  return false;
};


/**
 * Determine if we are able to add the supplied player to the lineup.
 * @param  {Object} player A player from the DraftGroupStore.
 * @return {bool}          Can the playe be added?
 */
const validatePlayer = (player, state) => {
  const errors = [];
  // Check if the player is already in the lineup.
  if (isPlayerInLineup(player, state)) {
    log.error('Selected player is already in the lineup.');
    errors.push('Selected player is already in the lineup');
    // return { errors: ['Selected player is already in the lineup'] };
  }

  // Check if there is room in the salary cap.
  // if (getTotalSalary(state) + player.salary > state.contestSalaryLimit) {
  //   console.error('Player exceeds maximum salary.')
  //   state.errorMessage = 'Player exceeds maximum salary'
  //   return false
  // }

  // Check if there is a valid slot for the player.
  if (!isSlotAvailableForPlayer(player, state)) {
    log.error('There is no slot available for this player.');
    errors.push('There is no slot available for this player');
  }

  // If all checks pass, the player can be added.
  return { errors };
};


const addPlayer = (player, state, callback) => {
  const playerErrors = validatePlayer(player, state);
  if (!playerErrors.errors.length) {
    const newLineup = insertPlayerIntoLineup(player, state);
    return callback(playerErrors.errors, newLineup);
  }

  return callback(playerErrors.errors, null);
};


/**
 * Remove a player from the lineup.
 * @param  {int} playerId the player.player_id to remove.
 */
const removePlayer = (playerId, state) => {
  // Loop through each lineup slot looking for the specified player. once found, set the
  // player property to null.
  for (const slot of state.lineup) {
    if (slot.player) {
      if (playerId === slot.player.player_id) {
        slot.player = null;
        return;
      }
    }
  }

  log.error('player not found in lineup!', playerId, state.lineup);
};


module.exports = (state = initialState, action) => {
  let newState = {};

  switch (action.type) {

    // Create an empty lineup card based on the roster of the sport of the current draftgroup.
    case ActionTypes.CREATE_LINEUP_INIT:
      // Return a copy of the previous state with our new things added to it.
      newState = merge({}, state, {
        lineup: rosterTemplates[action.sport],
        remainingSalary: salaryCaps[action.sport],
        contestSalaryLimit: salaryCaps[action.sport],
      });
      // After the state has a roster, find it's open positions.
      newState.availablePositions = findAvailablePositions(newState);
      newState.avgRemainingPlayerSalary = getAvgRemainingPlayerSalary(newState);

      // if the card is full, it can be saved.
      if (newState.availablePositions.length === 0) {
        newState.lineupCanBeSaved = true;
      } else {
        newState.lineupCanBeSaved = false;
      }

      return newState;


    // Add provided player to the new lineup
    case ActionTypes.CREATE_LINEUP_ADD_PLAYER:
      // if there is an error adding the player, return the state with an error message
      return addPlayer(action.player, state, (errors, updatedLineup) => {
        if (errors.length > 0) {
          return merge({}, state, {
            errorMessage: errors,
          });
        }
        // If we can add the player, add them and update the state.
        merge({}, state, { lineup: updatedLineup, errorMessage: null });
        newState = merge({}, state, {
          avgRemainingPlayerSalary: getAvgRemainingPlayerSalary(state),
          remainingSalary: getRemainingSalary(state),
          errorMessage: null,
        });
        // After the state's roster has been updated, find it's open positions.
        newState.availablePositions = findAvailablePositions(newState);

        // if the card is full, it can be saved.
        if (newState.availablePositions.length === 0) {
          newState.lineupCanBeSaved = true;
        } else {
          newState.lineupCanBeSaved = false;
        }

        setInProgressLocalLineup(newState.lineup, action.draftGroupId);
        return newState;
      });


    case ActionTypes.CREATE_LINEUP_REMOVE_PLAYER:
      newState = merge({}, state, {
        errorMessage: null,
      });
      removePlayer(action.playerId, newState);
      newState.avgRemainingPlayerSalary = getAvgRemainingPlayerSalary(newState);
      newState.remainingSalary = getRemainingSalary(newState);
      newState.availablePositions = findAvailablePositions(newState);

      // if the card is full, it can be saved.
      if (newState.availablePositions.length === 0) {
        newState.lineupCanBeSaved = true;
      } else {
        newState.lineupCanBeSaved = false;
      }

      setInProgressLocalLineup(newState.lineup, action.draftGroupId);
      return newState;


    case ActionTypes.CREATE_LINEUP_SAVE_FAIL:
      return merge({}, state, {
        errorMessage: action.err.detail,
      });


    case ActionTypes.CREATE_LINEUP_IMPORT:
      newState = merge({}, state);
      // We're passed a list of players. Make sure we're putting each one into the correct lineup
      // slot based on the idx property.
      forEach(newState.lineup, (slot, index) => {
        const playerToAdd = find(action.players, { idx: slot.idx });
        if (playerToAdd && playerToAdd.player_id) {
          newState.lineup[index].player = playerToAdd;
        }
      });

      // Update the title (optional)
      newState.lineupTitle = action.title;
      newState.avgRemainingPlayerSalary = getAvgRemainingPlayerSalary(newState);
      newState.remainingSalary = getRemainingSalary(newState);
      newState.availablePositions = findAvailablePositions(newState);

      // if the card is full, it can be saved.
      if (newState.availablePositions.length === 0) {
        newState.lineupCanBeSaved = true;
      } else {
        newState.lineupCanBeSaved = false;
      }

      return newState;


    default:
      return state;

  }
};
