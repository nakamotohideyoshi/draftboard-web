"use strict";

var AppActions = require('../../actions/app-actions');


/*
* Handles events for the hamburger menu.
*/
var HamburgerMenu = (function() {
  var attachedEventListener;

  var exports = {
    // Attach nav to DOM - this is a method in case we need to initialize elsewhere + needed for testing
    // return {boolean} whether or not the nav successfully attached to the DOM
    attachNavEventHandlers: function() {
      var el = document.querySelectorAll(".nav-main-trigger")[0];
      var navNode = document.querySelectorAll(".nav-main")[0];

      if (typeof el === 'undefined' || typeof navNode === 'undefined') {
        return false;
      }

      var isOpen = false;

      attachedEventListener = window.addEventListener('click', function(node) {
        if ((navNode.contains(node.target) === 0 && navNode !== node.target) && isOpen === true) {
          AppActions.closeNavMain();
          isOpen = false;
        } else if ((el.contains(node.target) === true || el === node.target) && isOpen === false) {
          AppActions.openNavMain();
          isOpen = true;
        }
      });

      return true;
    },

    // Removes the window click event handlers (used for testing only to date)
    removeNavEventHandlers: function() {
      attachedEventListener = null;
    }
  };

  // run on initial setup
  exports.attachNavEventHandlers();

  return exports;

})();


module.exports = HamburgerMenu;
