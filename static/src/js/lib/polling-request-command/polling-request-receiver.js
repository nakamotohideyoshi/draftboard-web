/* eslint no-use-before-define: "off" */

import log from '../logging.js';
import * as ContestPoolEntryCommand from './contest-pool-entry-command.js';
import * as LineupEditCommand from './lineup-edit-command.js';


/**
 * PollingRequestReceiver
 * This is a classic receiver in the Command pattern. It maintains queue of
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
    log.debug('command added.', commandQueue);
  }

  /**
   * Remove the current command from the queue.
   */
  function finishCurrentCommand() {
    if (commandQueue.length > 0) {
      commandQueue.shift();
    } else {
      log.warn('Cannot finishCurrentCommand, commandQueue is empty!', commandQueue);
    }
  }

  /**
   * Stat the next command (if one exists).
   */
  function startNextCommand() {
    if (commandQueue.length === 0) {
      log.debug('Cannot start next command, commandQueue is empty.');
      log.debug('setting running = false');
      running = false;
    } else {
      log.debug('Starting next command.');
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
    log.debug('fetchLoop()');
    running = true;

    task.command.fetch(task.taskId).then(() => {
      if (task.command.shouldFetch(task.taskId)) {
        window.setTimeout(fetchLoop, 500, task);
        return;
      }
      log.debug('fetchLoop() finished with a non-FAILURE fetch response');
      finishCurrentCommand();
      startNextCommand();
    }).catch((reason) => {
      log.debug('fetchLoop() finished due to \'FAILURE\' fetch response:', reason);
      finishCurrentCommand();
      startNextCommand();
    });
  }

  function run() {
    if (!running) {
      startNextCommand();
    } else {
      log.debug('run() ignored, Receiver is already running.');
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

    case 'LineupEditRequest':
      command = LineupEditCommand;
      break;

    default:
      log.error('Command type is not supported:', type);
      return;
  }

  log.info('adding polling request command', taskId);
  // Add the command to our receiver and tell it to start.
  PollingRequestReceiver.addCommand(command, taskId);
  PollingRequestReceiver.run();
}
