"use strict";
var path = require('path');
var baseConfig = require('./webpack-base.config.js');


// Override base configuration entries with those for the PRODUCTION build.
module.exports = baseConfig({
  debug: false,
  // An 'entry' is a compiled & bundled file.
  entry: {
    // Main app file.
    'app': [
      // Our app to be bundled.
      path.join(__dirname, "static", "src", "js", "app.jsx")
    ],
    // unauthenticated users - they get a slimmed down set of static files.
    'logged-out': [
      // Our app to be bundled.
      path.join(__dirname, "static", "src", "js", "app-logged-out.jsx")
    ]
  }
});
