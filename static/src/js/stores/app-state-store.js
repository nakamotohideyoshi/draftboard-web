var log = require('../lib/logging.js');


/*
* This component listens to the AppStateStore store and keeps the <body> tag's classes in sync with whatever
* the content of the store is.
*/
var AppStateClass = (function() {
  var bodyEl = document.querySelector("body");


  var exports = {
    // Sync up classes in the AppStateStore to the <body> tag.
    updateBodyClasses: function(classes) {
      log.debug("AppStateClass.updateBodyClasses()", classes);
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
    log.debug("AppStateStore.addClass()", className);
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
    console.log(this);
    this.removeClass('appstate--pane--open');
  },

  contestTypeFiltered: function() {
    this.addClass('appstate--contest-filters-open');
  }

};


module.exports = AppActions;
