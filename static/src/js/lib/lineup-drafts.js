import log from './logging';


/**
 * When a user is creating a lineup in the draft section, we want to save their
 * progress in localstorage. This way if they refresh the page or navigate away
 * they can pick up where they left off.
 *
 * The localstorage value is indexed by the draft group id.
 *
 * Whenever a user adds or removes a player, the lineup is saved back to
 * localStorage. When the lineup is saved on the server, we delete it from
 * localStorage.
 */

/**
 * Check if localstorage is available.
 *
 * via: https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API/Using_the_Web_Storage_API
 * @param type
 * @returns {boolean}
 */
function storageAvailable(type) {
  const storage = window[type];
  try {
    const x = '__storage_test__';
    storage.setItem(x, x);
    storage.removeItem(x);
    return true;
  } catch (e) {
    log.error(`${type} is not available!`);
    log.error(e);
    return e instanceof DOMException && (
      // everything except Firefox
      e.code === 22 ||
      // Firefox
      e.code === 1014 ||
      // test name field too, because code might not be present
      // everything except Firefox
      e.name === 'QuotaExceededError' ||
      // Firefox
      e.name === 'NS_ERROR_DOM_QUOTA_REACHED') &&
      // acknowledge QuotaExceededError only if there's something already stored
      storage.length !== 0;
  }
}

const localStoreKey = 'lineupDrafts';

/**
 * Save a lineup draft to localStorage.
 *
 * @param lineup
 * @param draftGroupId
 */
export const saveLineupDraft = (lineup, draftGroupId) => {
  if (!storageAvailable('localStorage')) {
    return;
  }
  window.localStorage.setItem(localStoreKey, JSON.stringify({
    [draftGroupId]: lineup,
  }));
};


/**
 * Grab all of the lineup drafts, delete the specified one, then save them back.
 *
 * @param draftGroupId
 */
export const deleteLineupDraft = (draftGroupId) => {
  log.info(`Removing in-progress lineup from draftgroup ${draftGroupId} from localstorage.`);
  if (!storageAvailable('localStorage')) {
    return;
  }
  // Get all of the drafts.
  const lineupDrafts = JSON.parse(window.localStorage.getItem(localStoreKey));
  // Remove the current one.
  delete lineupDrafts[draftGroupId];
  // Save the rest back.
  window.localStorage.setItem(localStoreKey, JSON.stringify(lineupDrafts));
};


/**
 * Get a specific lineupDraft based on it's draftgroupid.
 *
 * @param draftGroupId
 * @returns {{}}
 */
export const getLineupDraft = (draftGroupId) => {
  if (!draftGroupId) {
    return {};
  }
  let lineupDrafts = {};

  if (!storageAvailable('localStorage')) {
    return {};
  }
  if (window.localStorage.getItem(localStoreKey)) {
    lineupDrafts = JSON.parse(window.localStorage.getItem(localStoreKey));
  }

  if (lineupDrafts.hasOwnProperty(draftGroupId)) {
    return lineupDrafts[draftGroupId];
  }
  return {};
};
