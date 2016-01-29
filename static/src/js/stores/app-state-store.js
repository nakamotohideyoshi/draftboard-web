import log from '../lib/logging'
import { forEach as _forEach } from 'lodash'


/*
* This component listens to the AppStateStore store and keeps the <body> tag's classes in sync with whatever
* the content of the store is.
*/
var AppStateClass = (function() {
  var bodyEl = document.querySelector("body");


  var exports = {
    // Sync up classes in the AppStateStore to the <body> tag.
    updateBodyClasses: function(classes) {
      log.debug("AppStateClass.updateBodyClasses()", classes, bodyEl.className);
      // Remove any existing appstate classes
      bodyEl.className = bodyEl.className.replace(/appstate-\S*(?!\S)/g, "");
      // Add the current set.
      bodyEl.className = bodyEl.className.trim() + ' ' + classes.join(" ");
    }
  };

  return exports
})();


/*
* A store to keep track of our app's state. this works in conjunction with AppStateClass component to add
* CSS class names for the current app state to the <body> tag.
*
* Actions must be declared in AppActions before they be listened to here.
* */
var AppActions = {
  classes: [],

  /**
   * Add a class to the list
   *
   * @param {string} className The class to be added.
   */
  addClass: function(className) {
    log.trace("AppStateStore.addClass()", className);
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
  removeClass: function(className) {
    log.debug("AppStateStore.removeClass()", className);
    var index = this.classes.indexOf(className);
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
  toggleClass: function(className) {
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
  openNavMain: function() {
    this.addClass('appstate--nav-main--open');
  },

  // When the hamburger icon gets closed.
  closeNavMain: function() {
    this.removeClass('appstate--nav-main--open');
  },

  // Open the slideover pane.
  openPane: function() {
    this.addClass('appstate--pane--open');
  },

  // Close the slideover pane.
  closePane: function() {
    this.removeClass('appstate--pane--open');
  },

  openPlayerPane: function(side) {
    this.addClass('appstate--pane--player--' + side + '--open')
  },

  closePlayerPane: function(side) {
    this.removeClass('appstate--pane--player--' + side + '--open')
  },

  // Toggle the included class. If opening, then close all other live panes
  togglePlayerPane: function(side) {
    log.debug('AppStateStore.togglePlayerPane()')

    const className = 'appstate--pane--player--' + side + '--open'

    let possiblePanes = [
      'appstate--pane--player--left--open',
      'appstate--pane--player--right--open'
    ]

    // if already open, then just close that one
    if (this.classes.indexOf(className) > -1) {
      log.debug('Already open, closing', className)
      this.removeClass(className)

    // otherwise close all of the panes and then open that one
    } else {
      log.debug('Opening', className)
      _forEach(possiblePanes, (pane) => {
        this.removeClass(pane)
      })

      this.addClass(className)
    }
  },

  contestTypeFiltered: function() {
    this.addClass('appstate--contest-filters-open');
  },

  // Toggle the included class. If opening, then close all other live panes
  toggleLiveRightPane: function(className) {
    let possiblePanes = [
      'appstate--live-contests-pane--open',
      'appstate--live-standings-pane--open'
    ]

    if (this.classes.indexOf(className) > -1) {
      this.removeClass(className)
    } else {
      _forEach(possiblePanes, (pane) => {
        this.removeClass(pane)
      })

      this.addClass(className)
    }
  }

};


module.exports = AppActions;
