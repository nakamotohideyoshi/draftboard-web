"use strict";

// Pull in the main scss file.
require("app.scss");

//var config = require("config");
var React = require("react");
var log = require("lib/logging");


require("components/app-state-class");

// Add top-level react components to the app, any dependencies of those components will be loaded also.
var ContestTable = require("components/contest-list/contest-list.jsx");

if (document.querySelectorAll("#contest-table").length) {
  log.debug("React.rendering ContestTable into DOM.");
  React.render(<ContestTable />, document.getElementById("contest-table"));
}


require("components/contest-list/contest-list-item-detail.jsx");
