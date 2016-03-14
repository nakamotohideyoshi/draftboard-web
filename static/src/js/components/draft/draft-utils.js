import * as AppActions from '../../stores/app-state-store.js';


/**
 * Common utilty functions for the draft section.
 */


// Clear + focus the player search field. Used when a player is added or removed from the lineup.
export function focusSearchField() {
  const searchField = document.querySelectorAll('.cmp-collection-search-filter__input');
  if (searchField.length) {
    if (searchField[0].value !== '') {
      searchField[0].focus();
      AppActions.clearPlayerSearchField();
    }
  }
}
