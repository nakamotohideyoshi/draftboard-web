const path = require('path');
const baseConfig = require('./webpack-base.config.js');
const webpack = require('webpack');
const Dashboard = require('webpack-dashboard');
const DashboardPlugin = require('webpack-dashboard/plugin');
const dashboard = new Dashboard();


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
        path.join(__dirname, 'static', 'src', 'sass', 'homepage.scss'),
      ],
    },
    // Devserver config
    devServer: {
      contentBase: './build',
      noInfo: false,
      colors: true,
      host: '0.0.0.0',
      port: 8090,
      quiet: true, // lets WebpackDashboard do its thing
      // stats: 'errors-only'
    },
    debug: true,
    cache: true,
    devtool: 'cheap-module-source-map',
  }
);

/**
 * API_DOMAIN requires a scenario at the end of the URL. current options are ['nba-live', 'mlb-live']
 */
config.plugins = config.plugins.concat([
  new DashboardPlugin(dashboard.setData),
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
