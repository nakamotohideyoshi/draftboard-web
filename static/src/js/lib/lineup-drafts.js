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


const localStoreKey = 'lineupDrafts';

/**
 * Save a lineup draft to localStorage.
 *
 * @param lineup
 * @param draftGroupId
 */
export const saveLineupDraft = (lineup, draftGroupId) => {
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
  const lineupDrafts = JSON.parse(window.localStorage.getItem(localStoreKey));
  delete lineupDrafts[draftGroupId];
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

  if (window.localStorage.getItem(localStoreKey)) {
    lineupDrafts = JSON.parse(window.localStorage.getItem(localStoreKey));
  }

  if (lineupDrafts.hasOwnProperty(draftGroupId)) {
    return lineupDrafts[draftGroupId];
  }
  return {};
};
