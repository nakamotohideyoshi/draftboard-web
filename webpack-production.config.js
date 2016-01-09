'use strict';
var path = require('path');
var baseConfig = require('./webpack-base.config.js');
var webpack = require('webpack');


// Override base configuration entries with those for the PRODUCTION build.
var config = Object.assign(
  baseConfig,
  {
    debug: false,

    // An 'entry' is a compiled & bundled file.
    entry: {
      // Main app file.
      'app': [
        // Our app to be bundled.
        path.join(__dirname, 'static', 'src', 'js', 'app.jsx')
      ],
      // unauthenticated users - they get a slimmed down set of static files.
      'logged-out': [
        // Our app to be bundled.
        path.join(__dirname, 'static', 'src', 'js', 'app-logged-out.jsx')
      ]
    }
  }
);

config.plugins = config.plugins.concat([
  // removes a lot of debugging code in React
  new webpack.DefinePlugin({
    'process.env': {
      'NODE_ENV': JSON.stringify('production')
  }})
]);

module.exports = config