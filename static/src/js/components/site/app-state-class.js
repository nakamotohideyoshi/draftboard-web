"use strict";

var AppStateStore = require("../../stores/app-state-store");

/*
* This component listens to the AppStateStore store and keeps the <body> tag's classes in sync with whatever
* the content of the store is.
*/
var AppStateClass = (function() {
  var bodyEl = document.querySelector("body");


  var exports = {
    // Sync up classes in the AppStateStore to the <body> tag.
    updateBodyClasses: function(classes) {
      // Remove any existing appstate classes
      bodyEl.className = bodyEl.className.replace(/appstate-\S*(?!\S)/g, "");
      // Add the current set.
      bodyEl.className = bodyEl.className.trim() + ' ' + classes.join(" ");
    }
  };

  // Listen to changes from the AppStateStore store.
  AppStateStore.listen(exports.updateBodyClasses);

  return exports;

})();


module.exports = AppStateClass;
