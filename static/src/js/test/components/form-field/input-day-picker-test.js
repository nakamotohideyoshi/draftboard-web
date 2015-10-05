'use strict';

require('../../test-dom')();
var React = require('react/addons');
var InputDayPicker = require('../../../components/form-field/input-day-picker.jsx');
var expect = require('chai').expect;


describe("InputDayPicker Component", function() {

  beforeEach(function(done) {
    var self = this;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));

    this.componentComponent = React.render(
      <InputDayPicker onDaySelected={function() { return; }} />,
      this.targetElement,
      function() {
        self.componentElement = this.getDOMNode();
        done();
      }
    );
  });

  it("should render a span element", function() {
    expect(this.componentElement.tagName).to.equal('SPAN');
  });

  it("should have span and div inside the span", function() {
    expect(this.componentElement.childNodes[0].tagName).to.equal('SPAN');
    expect(this.componentElement.childNodes[1].tagName).to.equal('DIV');
  });

});
