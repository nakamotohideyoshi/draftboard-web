"use strict";

var React = require('react');
var MaskedInput = require('react-maskedinput');
var renderComponent = require('../../lib/render-component');


var SSNMaskedInput = React.createClass({

  getInitialState: function() {
    return ({
      state: {
        ssn: ''
      }
    });
  },


  /**
   * When the input changes, update based on the input mask react component
   * @param {e} the input element
   */
  _onChange: function(e) {
    var stateChange = {};
    stateChange[e.target.name] = e.target.value;
    this.setState(stateChange);
  },


  render: function() {
    return (
      <MaskedInput
        className="form-field__text-input"
        type="text"
        id="ssn"
        name="ssn"
        pattern="111\-11\-1111"
        size="11"
        placeholder="*** ** ****"
        onChange={this._onChange}
      />
    );
  }

});


// Render the component.
renderComponent(<SSNMaskedInput />, '.form-field__ssn-input-wrapper');

module.exports = SSNMaskedInput;
