'use strict';

var Reflux = require('reflux');


var KeypressActions = Reflux.createActions([
  'keypressJ',
  'keypressK',
  'keypressESC'
]);

var ignoredElements = [
  'INPUT',
  'TEXTAREA'
];

var keyCodeMap = {
  27: 'ESC',
  74: 'J',
  75: 'K'
};


document.onkeyup = function (e) {
  e = e || window.event;
  // If for whatever eason the browser doesn't give us an activeElement, assume body.
  var activeElement = document.activeElement || document.body;

  // Check that the user isn't focused in an ignored element, and that the key pressed
  // is in our map.
  if (ignoredElements.indexOf(activeElement.nodeName) === -1 &&
      keyCodeMap[e.keyCode] !== undefined
    ) {
    // Fire the corresponding reflux action.
    KeypressActions['keypress' + keyCodeMap[e.keyCode]].apply();
  }
};


module.exports = KeypressActions;
