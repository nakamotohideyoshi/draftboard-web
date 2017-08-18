const path = require('path');
const baseConfig = require('./webpack-base.config.js');
const webpack = require('webpack');

// Override base configuration entries with those for the PRODUCTION build.
const config = Object.assign(
  baseConfig,
  {
    output: {
      path: path.join(__dirname, 'static', 'build'),
      publicPath: 'http://localhost:8090/static/',
      filename: 'js/[name].js',
    },
    // An 'entry' is a compiled & bundled file.
    entry: {
      // Main app file.
      app: [
        // Enable Webpack's dev server hot reloads for this entry.
        'webpack/hot/dev-server',
        path.join(__dirname, 'static', 'src', 'js', 'app.jsx'),
      ],
      // separated homepage
      homepage: [
        // Enable Webpack's dev server hot reloads for this entry.
        'webpack/hot/dev-server',
        path.join(__dirname, 'static', 'src', 'sass', 'homepage.scss'),
      ],
      // Separate bundle for animation debugger
      'live-debugger-app': [
        // Enable Webpack's dev server hot reloads for this entry.
        'webpack/hot/dev-server',
        path.join(__dirname, 'static', 'src', 'js', 'live-debugger-app.jsx'),
      ],
    },
    // Devserver config
    devServer: {
      contentBase: './build',
      host: '0.0.0.0',
      port: 8090,
      clientLogLevel: 'info',
      noInfo: false,
      stats: {
        // Config for minimal console.log mess.
        assets: false,
        colors: true,
        version: false,
        hash: false,
        timings: false,
        chunks: true,
        chunkModules: false,
        children: false,
      },
    },
    cache: true,
    devtool: 'cheap-module-source-map',
  }
);

/**
 * API_DOMAIN requires a scenario at the end of the URL. current options are ['nba-live', 'mlb-live']
 */
config.plugins = config.plugins.concat([
  // removes a lot of debugging code in React
  new webpack.DefinePlugin({
    'process.env': {
      NODE_ENV: JSON.stringify('debug'),
      // API_DOMAIN: JSON.stringify('http://draftboard-api-sandbox.herokuapp.com/mlb-live'),
      // API_DOMAIN: JSON.stringify('http://localhost:5000/mlb-live'),
      API_DOMAIN: JSON.stringify(''),
    } }),
]);

module.exports = config;
