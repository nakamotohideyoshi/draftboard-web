
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
  // ... add whatever browser globals your tests might need ...
  global.window.dfs = {
    user: {},
    logLevel: 'warn',
  };
};
