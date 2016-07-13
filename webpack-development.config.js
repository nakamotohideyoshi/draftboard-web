const path = require('path');
const baseConfig = require('./webpack-base.config.js');
const webpack = require('webpack');


// Override base configuration entries with those for the PRODUCTION build.
const config = Object.assign(
  baseConfig,
  {
    // An 'entry' is a compiled & bundled file.
    entry: {
      // Main app file.
      app: [
        // Enable Webpack's dev server hot reloads for this entry.
        'webpack/hot/dev-server',
        path.join(__dirname, 'static', 'src', 'js', 'app.jsx'),
      ],
      // unauthenticated users - they get a slimmed down set of static files.
      'logged-out': [
        // Enable Webpack's dev server hot reloads for this entry.
        'webpack/hot/dev-server',
        path.join(__dirname, 'static', 'src', 'js', 'app-logged-out.jsx'),
      ],
      // separated homepage
      homepage: [
        // Enable Webpack's dev server hot reloads for this entry.
        'webpack/hot/dev-server',
        path.join(__dirname, 'static', 'src', 'sass', 'blocks', 'homepage.scss'),
      ],
    },
    // Devserver config
    devServer: {
      contentBase: './build',
      noInfo: false,
      colors: true,
      host: '0.0.0.0',
      port: 8090,
      // stats: 'errors-only'
    },
    debug: true,
    cache: true,
    devtool: 'eval-cheap-module-source-map',
  }
);


config.plugins = config.plugins.concat([
  // removes a lot of debugging code in React
  new webpack.DefinePlugin({
    'process.env': {
      NODE_ENV: JSON.stringify('debug'),
      // API_DOMAIN: JSON.stringify('http://draftboard-api-sandbox.herokuapp.com'),
      // API_DOMAIN: JSON.stringify('http://localhost:5000'),
      API_DOMAIN: JSON.stringify(''),
    } }),
]);

module.exports = config;
