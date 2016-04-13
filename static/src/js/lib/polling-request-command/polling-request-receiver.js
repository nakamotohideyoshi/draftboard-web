/* eslint no-use-before-define: "off" */

import log from '../logging.js';
import * as entryRequestActions from '../../actions/entry-request-actions.js';
import * as ContestPoolEntryCommand from './contest-pool-entry-command.js';


/**
 * PollingRequestReceiver
 * This is a classic receiver in the Command pattern. It maintains stack of
 * commands as commandQueue.
 *
 * When a lineup is saved, or a lineup is entered into a contest pool, it isn't
 * processed synchronously by the server, it is put into a job queue and the
 * status of the job is available to us via API. This means that when one of
 * these actions is performed, we then need to poll the server to find the
 * status until we get a failure or success.
 *
 * Because each of these 2 types of things (lineup creation and contest pool
 * entering) have slightly different logic, we use the PollingRequestReceiver
 * to do the actual polling task management, and the logic for each is contained
 * in a command (contest-pool-entry-command, ).
 *
 * For each Command in the queue, it will re-poll the server based on the rules
 * set in the Command.
 *
 * The PollingRequestReceiver expects a Command to have the following methods:
 *
 * getTaskState - get the task's state info from the app store.
 * shouldFetch -  based on the task's state, should we ask the server what the
 * 								status of our entry/lineup request is?
 * fetch - XHR to the server to find our entry/lineup request's status.
 */
const PollingRequestReceiver = (() => {
  // Our Command task queue.
  const commandQueue = [];
  let running = false;

  /**
   * Add a Command to the queue.
   * @param {Object} command [description]
   * @param {String} taskId  [description]
   */
  function addCommand(command, taskId) {
    commandQueue.push({ command, taskId });
  }

  /**
   * Remove the current command from the queue.
   */
  function finishCurrentCommand() {
    commandQueue.shift();
  }

  /**
   * Stat the next command (if one exists).
   */
  function startNextCommand() {
    log.trace('startNextCommand()');
    if (!commandQueue.length) {
      running = false;
    } else {
      const currentCommand = commandQueue[0];
      fetchLoop(currentCommand);
    }
  }

  /**
   * Since we are repeatedly polling the server, recursively call this to run
   * the current commands fetch() method.
   * @param  {Object} task A command in the commandQueue.
   */
  function fetchLoop(task) {
    log.trace('fetchLoop()');
    running = true;

    task.command.fetch(task.taskId).then(() => {
      if (task.command.shouldFetch(task.taskId)) {
        fetchLoop(task);
      }
      finishCurrentCommand();
      startNextCommand();
    });
  }

  function run() {
    if (!running) {
      startNextCommand();
    } else {
      log.warn('Receiver not running, no commands in queue.');
    }
  }

  // Public methods.
  return {
    run,
    addCommand,
  };
})();


/**
 * Take a command, pass it to the reciever and begin running the command.
 * @param {String} type What type of polling request is this? entryRequest | lineupSaveRequest
 * @param {String} taskId The id of the task that has been saved to the app's store.
 */
export function addPollingRequest(type, taskId) {
  // First, determine which Command strategy to use based on the `type` argument
  let command;

  switch (type) {
    case 'entryRequest':
      command = ContestPoolEntryCommand;
      break;
    default:
      log.error('Command type is not supported:', type);
      return;
  }

  log.info('adding polling request command', taskId);
  // Add the task's command info into the app store.
  entryRequestActions.addEntryRequestMonitor(command, taskId);
  // Add the command to our receiver and tell it to start.
  PollingRequestReceiver.addCommand(command, taskId);
  PollingRequestReceiver.run();
}
