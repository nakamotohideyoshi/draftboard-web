var path = require("path");
var ExtractTextPlugin = require("extract-text-webpack-plugin");


module.exports = {

  entry: {
    app: [
      // The dev server.
      "webpack/hot/dev-server",
      // Our app to be bundled.
      path.join(__dirname, "static/src/js/app.jsx")
    ]
  },

  output: {
    path: path.join(__dirname, "static/build"),
    publicPath: "/static/",
    filename: "js/[name].js"
  },

  // Add source maps inline.
  devtool: "source-map",

  module: {
    loaders: [
      // jsx loader
      {
        test: /\.jsx$/,
        loader: "jsx-loader"
      },
      // Transform sass into css & extract the text.
      {
        test: /\.scss$/,
        loader: ExtractTextPlugin.extract(
          // Activate source maps via loader query.
          "css?sourceMap!" +
          "sass?sourceMap"
        )
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
    })
  ],

  resolve: {
    extensions: ["", ".js", ".jsx", ".scss"],
    // Add in bower components + sass dirs.
    root: [
      path.join(__dirname, "bower_components"),
      path.join(__dirname, "static/src/js"),
      path.join(__dirname, "static/src/sass")
    ]
  }

};
