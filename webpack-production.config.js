const path = require('path');
const baseConfig = require('./webpack-base.config.js');
const webpack = require('webpack');


// Override base configuration entries with those for the PRODUCTION build.
const config = Object.assign(
  baseConfig,
  {
    // Enable sourcemaps
    devtool: 'source-map',
    debug: false,

    // An 'entry' is a compiled & bundled file.
    entry: {
      // Main app file.
      app: [
        // Our app to be bundled.
        path.join(__dirname, 'static', 'src', 'js', 'app.jsx'),
      ],
      // unauthenticated users - they get a slimmed down set of static files.
      'logged-out': [
        // Our app to be bundled.
        path.join(__dirname, 'static', 'src', 'js', 'app-logged-out.jsx'),
      ],
      // separated homepage
      homepage: [
        path.join(__dirname, 'static', 'src', 'sass', 'homepage.scss'),
      ],
      // Separate bundle for animation debugger
      'live-debugger-app': [
        path.join(__dirname, 'static', 'src', 'js', 'live-debugger-app.jsx'),
      ],
    },
  }
);

config.plugins = config.plugins.concat([
  // removes a lot of debugging code in React
  new webpack.DefinePlugin({
    'process.env': {
      NODE_ENV: JSON.stringify('production'),
    },
  }),
]);

module.exports = config;
