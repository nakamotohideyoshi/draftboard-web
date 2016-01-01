
/*
  Create a fake document for jsdom to insert our rendered components into.

  http://www.asbjornenge.com/wwc/testing_react_components.html
*/
"use strict";

module.exports = function(markup) {
  if (typeof document !== "undefined") { return; }

  var jsdom = require("jsdom").jsdom;
  global.document = jsdom(markup || "<!doctype html><html><body></body></html>");
  global.window = document.defaultView;
  global.navigator = {
    userAgent: "node.js"
  };
  global.window.dfs = {
    user: {}
  }
  // ... add whatever browser globals your tests might need ...
};
