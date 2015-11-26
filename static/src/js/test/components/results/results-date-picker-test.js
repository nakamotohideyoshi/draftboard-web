'use strict';

require('../../test-dom')();
const React = require('react');
const ReactDOM = require('react-dom');
const ReactTestUtils = require('react-addons-test-utils');
const ResultsDatePicker = require('../../../components/results/results-date-picker.jsx');
const expect = require('chai').expect;

let selectedDate = null;
const defaultProps = {
  year:  2015,
  month: 1,
  day:   1,
  onSelectDate(year, month, day) {
    selectedDate = [year, month, day];
  }
};

describe("ResultsDatePicker Component", function() {

  beforeEach(function(done) {
    var self = this;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.component = ReactDOM.render(
      React.createElement(ResultsDatePicker, defaultProps),
      this.targetElement,
      function() {
        // Once it has been rendered...
        // Grab it from the DOM.
        self.componentElement = ReactDOM.findDOMNode(this);
        done();
      }
    );
  });

  afterEach(function() {
    document.body.innerHTML = '';
  });

  it('should be hidden by default and able to show/hide', function() {
    expect(this.componentElement.tagName).to.equal('DIV');

    expect(
      this.componentElement.querySelectorAll('.date-picker').length
    ).to.equal(0);

    ReactTestUtils.Simulate.click(
      this.componentElement.querySelector('.toggle')
    );

    expect(
      this.componentElement.querySelectorAll('.date-picker').length
    ).to.equal(1);

    document.body.click();

    expect(
      this.componentElement.querySelectorAll('.date-picker').length
    ).to.equal(0);
  });
});
