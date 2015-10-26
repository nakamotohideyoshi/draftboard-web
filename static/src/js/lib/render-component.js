'use strict';
var ReactDOM = require('react-dom');
var log = require("./logging");

/**
 * Render a React Component to all instances of the given DOM selector.
 * @param  {string} selector  A css-style dom selector.
 * @param  {Object} component A React comopnent instance.
 */
module.exports = function(component, selector) {

  // Query all matching DOM elements.
  var elements = document.querySelectorAll(selector);

  // Render the component on each existing DOM element.
  for (var i = 0; i < elements.length; i++) {
    log.debug('Rendering component: ' + component.type.displayName);
    ReactDOM.render(component, elements[i]);
  }

};
