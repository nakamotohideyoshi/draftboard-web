"use strict";

var baseConfig = require('./webpack-base.config.js');


// Override base configuration entries with those specific to the webpack devserver.
module.exports = baseConfig({
  debug: true,
  cache: true,
  devtool: "source-map"
});
