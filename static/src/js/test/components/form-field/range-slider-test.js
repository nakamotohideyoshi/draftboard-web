'use strict';
var sinon = require("sinon");
var onChangeSpy = sinon.spy(function() {
  return true;
});

require('../../test-dom')();
var React = require('react');
import ReactDOM from 'react-dom';
var RangeSliderComponent = require('../../../components/form-field/range-slider.jsx');
var expect = require('chai').expect;


/**
 * I think it's safe to rely on the library's built-in tests for most things, I'm just going to
 * test if the component mounts and the noUiSlider range slider gets rendered.
  */
describe('RangeSliderComponent Component', function() {

  beforeEach(function(done) {
    var self = this;
    document.body.innerHTML = '';

    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.SliderComponent = ReactDOM.render(
      <RangeSliderComponent
        minValLimit = {0}
        maxValLimit = {100}
        onChange = {onChangeSpy}
      />,
      this.targetElement,
      function() {
        // Once it has been rendered...
        // Grab it from the DOM.
        self.RangeSliderElement = ReactDOM.findDOMNode(this);
        done();
      }
    );
  });


  afterEach(function() {
    // Remove component from the DOM and empty the DOM for good measure.
    document.body.innerHTML = '';
  });


  it('should instantiate the noUiSlider plugin', function() {
    expect(this.RangeSliderElement.querySelectorAll('.noUi-target').length).to.equal(1);
  });


  it('should call the provided onChange method when a slider value changes', function() {
    this.SliderComponent.handleValueChange(0, 5, function() {
      sinon.assert.calledOnce(onChangeSpy);
    });
  });
});
