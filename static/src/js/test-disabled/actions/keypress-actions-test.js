'use strict';

require('../test-dom')();
var expect = require('chai').expect;
var sinon = require('sinon');
var KeypressActions = require('../../actions/keypress-actions.js');


var dispatchKeyboardEvent = function(keyCode) {
  // Manually press a key.
  var evt = document.createEvent("KeyboardEvent");
  evt.keyCode = keyCode;
  evt.initEvent("keyup", true, true);
  document.body.dispatchEvent(evt);
};


describe('KeypressActions Action', function() {

  it("should fire an action function when a key in the keyCodeMap is pressed", function() {
    var keyCodeMap = {
      27: 'ESC',
      74: 'J',
      75: 'K'
    };

    // For each key in the map, setup a spy, dispatch a keyboard event, and check that
    // the appropriate KeyPressAction was fired.
    for (var keyCode in keyCodeMap){
      var spy = sinon.spy(KeypressActions, 'keypress' + keyCodeMap[keyCode]);
      dispatchKeyboardEvent(keyCode);
      expect(spy.callCount).to.equal(1);
    }
  });

});
