"use strict";

var AppActions = require('actions/app-actions');


/*
* Handles events for the hamburger menu.
*/
var HamburgerMenu = (function() {
  var el = document.querySelectorAll(".nav-main--hamburglar")[0];

  if (typeof el !== 'undefined') {
    el.addEventListener('click', function() {
      AppActions.openNavMain();
    });
  }

})();


module.exports = HamburgerMenu;
