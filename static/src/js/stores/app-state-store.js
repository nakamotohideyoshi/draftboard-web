"use strict";

var Reflux = require("reflux");
var AppActions = require("../actions/app-actions");

/*
* A store to keep track of our app's state. this works in conjunction with AppStateClass component to add
* CSS class names for the current app state to the <body> tag.
*
* Actions must be declared in AppActions before they be listened to here.
* */

var AppStateStore = Reflux.createStore({
  classes: [],

  init: function() {
    this.listenTo(AppActions.somethingOn, this.onSomething);
  },

  addClass: function(className) {
    // If the class isn't already in our list, add it.
    if (this.classes.indexOf(className) === -1) {
      this.classes.push(className);
      this.trigger(this.classes);
    }
  },

  onSomething: function() {
    this.addClass("appstate-something");
  }

});


module.exports = AppStateStore;
