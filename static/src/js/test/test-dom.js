/*
  Create a fake document for jsdom to insert our rendered components into.

  http://www.asbjornenge.com/wwc/testing_react_components.html
*/
module.exports = (markup) => {
  if (typeof document !== 'undefined') { return; }
  const jsdom = require('jsdom').jsdom;

  global.document = jsdom(markup || '<!doctype html><html><body></body></html>');
  global.window = document.defaultView;
  global.navigator = {
    userAgent: 'node.js',
  };
  /**
   * `new Image` barfs an error.
   * I think it's doing this because there is no Image support in node.
   */
  global.Image = () => {
    console.warn('Warning: The `Image` method is being mocked from test-dom.js.');
  };

  // ... add whatever browser globals your tests might need ...
  global.window.dfs = {
    user: {},
    logLevel: 'warn',
    replayerTimeDelta: 0,
    playerImagesBaseUrl: 'http://localhost',
  };
};
