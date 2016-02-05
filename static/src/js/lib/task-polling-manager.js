// import Raven from 'raven-js';
import 'babel-core/polyfill';
// so we can use superagent with Promises
import log from '../lib/logging.js';
import store from '../store.js';


// TODO: Pull shared logic from lineup entry + save actions into here.


// A place to store setInterval IDs. This should probably be put in the store instead.
const entryMonitors = [];
// When polling, how many milleseconds should we continue to poll for before giving up?
// const maxRetrytime = 10000; // 10 seconds
// How often should we attemt to re-poll?
const minimumPollInterval = 250;


/**
 * Clear the loop that repeatedly attempts to check the status of an entry.
 * @param  {[type]} taskId [description]
 * @return {[type]}        [description]
 */
export function clearTaskMonitor(taskId) {
  log.debug(`Clearing monitor for task ${taskId}`);
  window.clearInterval(entryMonitors[taskId].loop);
}


function fetchIfNeeded(taskId, shouldFetch, fetch) {
  if (shouldFetch(taskId)) {
    fetch(taskId)
  }
}


export function addTaskMonitor(taskId, taskAdded, shouldFetch, fetch, options = {}) {
  store.dispatch(taskAdded(taskId));

  // Create a monitor to repeatedly poll the entry status api.
  entryMonitors[taskId] = {};
  entryMonitors[taskId].options = options;

  if (shouldFetch) {
    fetch()
  }

  // Create a monitor loop that will contantly attempt to re-fetch the status of the entry.
  entryMonitors[taskId].loop = window.setInterval(
      () => fetchIfNeeded(taskId, shouldFetch, fetch),
     minimumPollInterval
  );
  log.info('monitoring entry request: ', entryMonitors[taskId]);
}
