import * as AppActions from '../../stores/app-state-store.js';


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
