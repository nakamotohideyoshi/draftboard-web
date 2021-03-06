import log from '../lib/logging';
import forEach from 'lodash/forEach';
import PubSub from 'pubsub-js';

// get custom logger for actions
const logAppStateChange = log.getLogger('app-state-store');


/*
* This component listens to the AppStateStore store and keeps the <body> tag's classes in sync with whatever
* the content of the store is.
*/
const AppStateClass = (() => {
  const bodyEl = document.querySelector('body');


  const exports = {
    // Sync up classes in the AppStateStore to the <body> tag.
    updateBodyClasses: (classes) => {
      logAppStateChange.debug('app-state-store.updateBodyClasses', classes, bodyEl.className);

      // Remove any existing appstate classes
      bodyEl.className = bodyEl.className.replace(/appstate-\S*(?!\S)/g, '');
      // Add the current set.
      bodyEl.className = `${bodyEl.className.trim()} ${classes.join(' ')}`;
    },
  };

  return exports;
})();


/*
* A store to keep track of our app's state. this works in conjunction with AppStateClass component to add
* CSS class names for the current app state to the <body> tag.
*
* Actions must be declared in AppActions before they be listened to here.
* */
const AppActions = {
  classes: [],

  /**
   * Add a class to the list
   *
   * @param {string} className The class to be added.
   */
  addClass(className) {
    logAppStateChange.debug('app-state-store.addClass', className);

    // If the class isn't already in our list, add it.
    if (this.classes.indexOf(className) === -1) {
      this.classes.push(className);
      AppStateClass.updateBodyClasses(this.classes);
    }
  },


  /**
   * Remove a class from the list.
   * @param  {string} className Class to be removed
   */
  removeClass(className) {
    logAppStateChange.debug('app-state-store.removeClass', className);

    const index = this.classes.indexOf(className);
    // If the class is in the list, delete it.
    if (index > -1) {
      this.classes.splice(index, 1);
      AppStateClass.updateBodyClasses(this.classes);
    }
  },


  /**
   * Toggles a classname from the list
   * @param  {string} className Class to be toggled
   */
  toggleClass(className) {
    logAppStateChange.debug('app-state-store.toggleClass', className);

    if (this.classes.indexOf(className) === -1) {
      this.addClass(className);
    } else {
      this.removeClass(className);
    }
  },


  /**
   * Actions - NOTE: These might make more sense being somewhere else.
   */

  // When the hamburger icon gets opened.
  openNavMain() {
    this.addClass('appstate--nav-main--open');
  },

  // When the hamburger icon gets closed.
  closeNavMain() {
    this.removeClass('appstate--nav-main--open');
  },

  // Open the slideover pane.
  openPane() {
    this.addClass('appstate--pane--open');
    PubSub.publish('pane.open');
  },

  // Close the slideover pane.
  closePane() {
    this.removeClass('appstate--pane--open');
    PubSub.publish('pane.close');
  },

  openPlayerPane(side) {
    this.addClass(`appstate--pane--player--${side}--open`);
  },

  closePlayerPane(side) {
    this.removeClass(`appstate--pane--player--${side}--open`);
  },

  // Toggle the included class. If opening, then close all other live panes
  togglePlayerPane(side) {
    logAppStateChange.debug('app-state-store.togglePlayerPane', side);

    const className = `appstate--pane--player--${side}--open`;

    const possiblePanes = [
      'appstate--pane--player--left--open',
      'appstate--pane--player--right--open',
    ];

    // if already open, then just close that one
    if (this.classes.indexOf(className) > -1) {
      log.debug('Already open, closing', className);
      this.removeClass(className);

    // otherwise close all of the panes and then open that one
    } else {
      log.debug('Opening', className);
      forEach(possiblePanes, (pane) => {
        this.removeClass(pane);
      });

      this.addClass(className);
    }
  },

  // Toggle the included class. If opening, then close all other live panes
  toggleLiveRightPane(className) {
    const possiblePanes = [
      'appstate--live-contests-pane--open',
      'appstate--live-standings-pane--open',
    ];

    if (this.classes.indexOf(className) > -1) {
      this.removeClass(className);
    } else {
      forEach(possiblePanes, (pane) => {
        this.removeClass(pane);
      });

      this.addClass(className);
    }
  },

  enterContestButtonMouseOver() {
    this.addClass('appstate-enterContestButtonHover');
  },


  enterContestButtonMouseOut() {
    this.removeClass('appstate-enterContestButtonHover');
  },


  modalOpened() {
    this.addClass('appstate-modal-open');
  },


  modalClosed() {
    this.removeClass('appstate-modal-open');
  },


  clearPlayerSearchField() {
    PubSub.publish('playerSearch.clear');
  },

  // When the user clicks the background overlay div of the modal this event will fire.
  // If you want to take action when this happens, subscribe to it in your component and react
  // accordingly. I didn't set this to close the modal by default because I'm not sure that is
  // always what is desired.
  //
  // edit: I'm not even sure this belongs here, since it's essentially just a wrapper on the
  // pubSub event. Though I kinda like that all global app-wide actions are in this file. Whatevs.
  modalBgClick() {
    PubSub.publish('modal.bgClick');
  },

};


module.exports = AppActions;
