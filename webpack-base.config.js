const path = require('path');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const WebpackNotifierPlugin = require('webpack-notifier');
const webpack = require('webpack');
const autoprefixer = require('autoprefixer');


module.exports = {

  // Configure the output of compiled entry files.
  output: {
    path: path.join(__dirname, 'static', 'build'),
    publicPath: '/static/',
    filename: 'js/[name].js',
  },

  module: {
    loaders: [
      // jsx loader - to convert jsx to native js.
      // Check .babelrc for more config.
      {
        test: /(\.jsx|\.js)$/,
        loader: 'babel-loader',
        exclude: /node_modules/,
        query: {
          // https://github.com/babel/babel-loader#options
          cacheDirectory: true,
        },
      },
      // Transform sass into css & extract the text.
      {
        test: /\.scss$/,
        loader: ExtractTextPlugin.extract(
          'css-loader?sourceMap!' +
          'postcss-loader!' +
          'sass-loader?sourceMap'
        ),
      },
      // Run ESLint on jsx + js files.
      {
        test: /(\.jsx|\.js)$/,
        loader: 'eslint-loader',
        exclude: /node_modules/,
      },
      // Images under 8KB made inline base64
      {
        test: /\.(png|jpe?g|gif)$/,
        loader: 'url-loader?name=img/[name]-[sha512:hash:base64:7].[ext]&limit=8192',
      },
      {
        test: /\.(svg)$/i,
        loaders: [
          'file-loader?name=img/[name]-[sha512:hash:base64:7].[ext]',
        ],
      },
      {
        test: /\.json$/,
        loader: 'json-loader',
      },
      {
        test: /\.txt$/,
        loader: 'raw-loader',
      },
    ],
  },

  postcss: [
    autoprefixer({ browsers: ['last 2 versions'] }),
  ],

  plugins: [
    // Extract css text and save to file.
    new ExtractTextPlugin('css/[name].css', {
      allChunks: false,
    }),
    // Build error notifications.
    new WebpackNotifierPlugin({
      title: 'Webpack',
      contentImage: 'https://dl.dropboxusercontent.com/spa/wn0oryty1do7jho/rq03wbw9.png',
    }),
    // Don't let Moment (and presumably other libs) load in their full locale info - it's a lot.
    // https://github.com/webpack/webpack/issues/198#issuecomment-124924974
    // new webpack.ContextReplacementPlugin(/.*$/, /NEVER_MATCH^/),
    // Let moment load just selected languages
    new webpack.ContextReplacementPlugin(/moment[\\\/]locale$/, /^\.\/(en-gb)$/),

    // new webpack.ProvidePlugin({
    //   moment: "moment"
    // })
  ],

  // Tell webpack where to look for require()'d files. If it can't locate a file, make sure you're
  //  requiring it relative to one of these paths, and that the file extension is allowed.
  resolve: {
    extensions: ['', '.js', '.jsx', '.scss'],
    // Add in bower components + sass dirs.
    root: [
      path.join(__dirname, 'static', 'src', 'js'),
      path.join(__dirname, 'static', 'src', 'sass'),
    ],
  },

  eslint: {
    // ESLint configuration file location.
    configFile: '.eslintrc',
    // Add a nicer readout formatter.
    formatter: require('eslint-friendly-formatter'),
  },
};
