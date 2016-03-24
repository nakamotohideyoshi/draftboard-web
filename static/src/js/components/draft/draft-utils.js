import * as AppActions from '../../stores/app-state-store.js';
import { filter as _filter } from 'lodash';

/**
 * Common utilty functions for the draft section.
 */


// Clear + focus the player search field. Used when a player is added or removed from the lineup.
export function focusPlayerSearchField() {
  // Get the input field, if it is active.
  const searchField = document.querySelectorAll(
    '.cmp-collection-search-filter--active .cmp-collection-search-filter__input'
  );
  // focus it.
  if (searchField.length) {
    searchField[0].focus();
  }
}

// Clear the value from the player search field
export function clearPlayerSearchField() {
  AppActions.clearPlayerSearchField();
}


// Determine whether a supplied player is in the lineup.
export function isPlayerInLineup(lineup, player) {
  // Return a list of all matching players.
  const matchingPlayers = _filter(lineup, (slot) => {
    if (slot.player) {
      if (slot.player.player_id === player.player_id) {
        return true;
      }
    }
    return false;
  });

  // If the list of matching players is empty, the player is not in the lineup.
  return Object.keys(matchingPlayers).length > 0;
}
