"use strict";

var AppActions = require('../../actions/app-actions');


/*
* Handles events for the hamburger menu.
*/
var HamburgerMenu = (function() {
  var el = document.querySelectorAll(".nav-main-trigger")[0];
  var navNode = document.querySelectorAll(".nav-main")[0];

  if (typeof el !== 'undefined') {
    var isOpen = false;

    window.addEventListener('click', function(node) {
      if (navNode.contains(node.target) === false && isOpen === true) {
        AppActions.closeNavMain();
        isOpen = false;
      }

      if (el.contains(node.target) === true && isOpen === false) {
        AppActions.openNavMain();
        isOpen = true;
      }
    });
  }

})();


module.exports = HamburgerMenu;
