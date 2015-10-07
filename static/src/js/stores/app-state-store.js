"use strict";

var Reflux = require('reflux');
var AppActions = require('../actions/app-actions');
var ContestActions = require('../actions/contest-actions.js');
var log = require('../lib/logging.js');


/*
* A store to keep track of our app's state. this works in conjunction with AppStateClass component to add
* CSS class names for the current app state to the <body> tag.
*
* Actions must be declared in AppActions before they be listened to here.
* */
var AppStateStore = Reflux.createStore({
  classes: [],

  init: function() {
    // Connect AppActions to methods in this store.
    this.listenTo(AppActions.openNavMain, this.onOpenNavMain);
    this.listenTo(AppActions.closeNavMain, this.onCloseNavMain);
    this.listenTo(AppActions.openPane, this.onOpenPane);
    this.listenTo(AppActions.closePane, this.onClosePane);
    this.listenTo(ContestActions.contestTypeFiltered, this.onContestTypeFiltered);
  },


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
      this.trigger(this.classes);
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
      this.trigger(this.classes);
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
  onOpenNavMain: function() {
    this.addClass('appstate--nav-main--open');
  },

  // When the hamburger icon gets closed.
  onCloseNavMain: function() {
    this.removeClass('appstate--nav-main--open');
  },

  // Open the slideover pane.
  onOpenPane: function() {
    this.addClass('appstate--pane--open');
  },

  // Close the slideover pane.
  onClosePane: function() {
    this.removeClass('appstate--pane--open');
  },

  onContestTypeFiltered: function() {
    this.addClass('appstate--contest-filters-open');
  }

});


module.exports = AppStateStore;
