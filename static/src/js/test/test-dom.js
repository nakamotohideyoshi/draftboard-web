/*
  Create a fake document for jsdom to insert our rendered components into.

  http://www.asbjornenge.com/wwc/testing_react_components.html
*/
module.exports = (markup) => {
  if (typeof document !== 'undefined') { return; }
  const jsdom = require('jsdom').jsdom;
  // Needed for the braintree-web package.
  global.Braintree = {};
  // the second parameter for url is because of react-router-redux, see https://goo.gl/pDwoDa
  global.document = jsdom(markup || '<!doctype html><html><body></body></html>', { url: 'http://localhost' });
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

  // per https://github.com/akiran/react-slick/issues/93
  window.matchMedia = window.matchMedia || function matchMedia() {
    return {
      matches: false,
      addListener: () => ({}),
      removeListener: () => ({}),
    };
  };


  // ... add whatever browser globals your tests might need ...
  global.window.dfs = {
    user: {
      pusher_key: 'NONE',
      pusher_channel_prefix: 'test',
    },
    logLevel: 'warn',
    replayerTimeDelta: 0,
    playerImagesBaseUrl: 'http://localhost',
  };
};
