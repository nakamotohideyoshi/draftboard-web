'use strict';

var path = require('path');
var _ = require('lodash');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var WebpackNotifierPlugin = require('webpack-notifier');
var webpack = require('webpack');


module.exports = function(options) {
  var defaultConfig = {
    // An 'entry' is a compiled & bundled file.
    entry: {
      // Main app file.
      'app': [
        // Enable Webpack's dev server hot reloads for this entry.
        'webpack/hot/dev-server',
        path.join(__dirname, 'static', 'src', 'js', 'app.jsx')
      ],
      // unauthenticated users - they get a slimmed down set of static files.
      'logged-out': [
        // Enable Webpack's dev server hot reloads for this entry.
        'webpack/hot/dev-server',
        path.join(__dirname, 'static', 'src', 'js', 'app-logged-out.jsx')
      ]
    },

    // Configure the output of compiled entry files.
    output: {
      path: path.join(__dirname, 'static', 'build'),
      publicPath: '/static/',
      filename: 'js/[name].js'
    },

    // Devserver config
    devServer: {
      contentBase: './build',
      noInfo: false,
      colors: true,
      host: '0.0.0.0',
      port: 8090,
      stats: {
        cached: true
      }
    },

    module: {
      loaders: [
        // jsx loader - to convert jsx to native js.
        {
          test: /\.jsx?$/,
          exclude: /node_modules/,
          loader: 'babel-loader'
        },
        // Transform sass into css & extract the text.
        {
          test: /\.scss$/,
          loader: ExtractTextPlugin.extract(
            'css-loader?sourceMap!' +
            'autoprefixer-loader?browsers=last 2 version!' +
            'sass-loader?sourceMap'
          )
        },
        // Run ESLint on jsx + js files.
        {
          test: /(\.jsx|\.js)$/,
          loader: 'eslint-loader',
          exclude: /node_modules/
        },
        // Images.
        {
            test: /\.(jpe?g|png|gif|svg)$/i,
            loaders: [
              // Optimize image files, and move them to the build directory.
              'file-loader?name=img/[name]-[sha512:hash:base64:7].[ext]',
              'image-webpack?bypassOnDebug=true&optimizationLevel=0'
            ]
        }
      ]
    },

    plugins: [
      // Extract css text and save to file.
      new ExtractTextPlugin('css/[name].css', {
        allChunks: false
      }),
      // Build error notifications.
      new WebpackNotifierPlugin({
        title: 'Webpack',
        contentImage: 'https://dl.dropboxusercontent.com/spa/wn0oryty1do7jho/rq03wbw9.png'
      }),
      // Don't let Moment (and presumably other libs) load in their full locale info - it's a lot.
      // https://github.com/webpack/webpack/issues/198#issuecomment-124924974
      new webpack.ContextReplacementPlugin(/.*$/, /NEVER_MATCH^/)
    ],

    // Tell webpack where to look for require()'d files. If it can't locate a file, make sure you're
    //  requiring it relative to one of these paths, and that the file extension is allowed.
    resolve: {
      extensions: ['', '.js', '.jsx', '.scss'],
      // Add in bower components + sass dirs.
      root: [
        //path.join(__dirname, 'bower_components'),
        path.join(__dirname, 'static', 'src', 'js'),
        path.join(__dirname, 'static', 'src', 'sass')
      ]
    },

    eslint: {
      // ESLint configuration file location.
      configFile: '.eslintrc',
      // Add a nicer readout formatter.
      formatter: require('eslint-friendly-formatter')
    }
  };

  // Overwrite any default values with the provided options.
  return _.extend(defaultConfig, options);

};
