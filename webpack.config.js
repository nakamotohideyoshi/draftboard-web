var path = require("path");
var ExtractTextPlugin = require("extract-text-webpack-plugin");
var WebpackNotifierPlugin = require('webpack-notifier');
var webpack = require("webpack");

module.exports = {

  // An 'entry' is a compiled & bundled file.
  entry: {
    // Main app file.
    app: [
      // Enable Webpack's dev server hot reloads for this entry.
      "webpack/hot/dev-server",
      // Our app to be bundled.
      path.join(__dirname, "static/src/js/app.jsx")
    ]
  },

  // Configure the output of compiled entry files.
  output: {
    path: path.join(__dirname, "static/build"),
    publicPath: "/static/",
    filename: "js/[name].js"
  },

  module: {
    loaders: [
      // jsx loader - to convert jsx to native js.
      {
        test: /\.jsx$/,
        loader: "jsx-loader"
      },
      // Transform sass into css & extract the text.
      {
        test: /\.scss$/,
        loader: ExtractTextPlugin.extract(
          "css!sass"
        )
      },
      // Run ESLint on jsx + js files.
      {
        test: /(\.jsx|\.js)$/,
        loader: "eslint-loader",
        exclude: /node_modules/
      }

    ]
  },

  plugins: [
    // Add resolve plugin for module discovery.
    //new webpack.ResolverPlugin(
    //  new webpack.ResolverPlugin.DirectoryDescriptionFilePlugin("bower.json", ["main"])
    //),
    // Extract css text and save to file.
    new ExtractTextPlugin("css/[name].css", {
      allChunks: false
    }),
    // Build error notifications.
    new WebpackNotifierPlugin({
      title: "Webpack",
      contentImage: "https://dl.dropboxusercontent.com/spa/wn0oryty1do7jho/rq03wbw9.png"
    }),
    // Remove comments in js when uglifying.
    //new webpack.optimize.UglifyJsPlugin({ output: {comments: false} })
  ],

  // Tell webpack where to look for require()'d files. If it can't locate a file, make sure you're requiring it
  // relative to one of these paths, and that the file extension is allowed.
  resolve: {
    extensions: ["", ".js", ".jsx", ".scss"],
    // Add in bower components + sass dirs.
    root: [
      //path.join(__dirname, "bower_components"),
      path.join(__dirname, "static/src/js"),
      path.join(__dirname, "static/src/sass")
    ]
  },

  eslint: {
    // ESLint configuration file location.
    configFile: ".eslintrc",
    // Add a nicer readout formatter.
    formatter: require("eslint-friendly-formatter")
  }

};
