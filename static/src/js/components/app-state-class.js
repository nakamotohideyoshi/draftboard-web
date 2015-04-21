"use strict";

var AppStateStore = require("../stores/app-state-store");

/*
* This component listens to the AppStateStore store and keeps the <body> tag's classes in sync with whatever
* the content of the store is.
*/
var AppStateClass = (function() {

  AppStateStore.listen(function(data) {
    var bodyEl = document.querySelector("body");
    // Remove any existing appstate classes
    bodyEl.className = bodyEl.className.replace(/appstate-\S*(?!\S)/g, "");
    // Add the current set.
    bodyEl.className = data.join(" ");
  });

})();


module.exports = AppStateClass;
