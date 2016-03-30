'use strict';

require('../../test-dom')();
var React = require('react');
var Component = require('../../../components/contest-list/contest-range-slider-filter.jsx');
var expect = require('chai').expect;
var sinon = require("sinon");
var onMount = function() {};
var onUpdateSpy = sinon.spy(function() {});


describe('CollectionRangeSliderFilter Component', function() {

  beforeEach(function(done) {
    var self = this;

    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.component = React.render(
      <Component
        filterProperty='name'
        filterName='test'
        onUpdate={onUpdateSpy}
        onMount={onMount}
      />,
      this.targetElement,
      function() {
        // Once it has been rendered...
        // Grab it from the DOM.
        self.domElement = this.getDOMNode();
        done();
      }
    );
  });


  afterEach(function() {
    // Remove component from the DOM and empty the DOM for good measure.
    document.body.innerHTML = '';
  });


  it('should instantiate the noUiSlider plugin', function() {
    expect(this.domElement.querySelectorAll('.noUi-target').length).to.equal(1);
  });


  // it('should filter rows based on a value range', function() {
  //   var testRow = {
  //     'buyin': '50.00'
  //   };
  //
  //   this.component.setState({
  //     match: {
  //       minVal: 1,
  //       maxVal: 100
  //     }
  //   }, function() {
  //     expect(this.component.filter(testRow)).to.equal(true);
  //   }.bind(this));
  //
  //   this.component.setState({
  //     match: {
  //       minVal: 51,
  //       maxVal: 100
  //     }
  //   }, function() {
  //     expect(this.component.filter(testRow)).to.equal(false);
  //   }.bind(this));
  // });


  it('should alert the Contest Store that something has changed via an action', function() {
    this.component.handleChange({
      match: {
        minVal: 99,
        maxVal: 100
      }
    });

    sinon.assert.calledOnce(onUpdateSpy);
  });
});
