'use strict';

require('../../test-dom')();
const React = require('react');
const ReactDOM = require('react-dom');
const ReactTestUtils = require('react-addons-test-utils');
import DatePicker from '../../../components/site/date-picker.jsx';
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

describe("DatePicker Component", function() {

  beforeEach(function(done) {
    var self = this;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.component = ReactDOM.render(
      React.createElement(DatePicker, defaultProps),
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

  it('should render properly selected month', function() {
    expect(this.componentElement.tagName).to.equal('DIV');

    // First 6 days are from January.
    [].slice.call(
      this.componentElement.querySelectorAll('tbody td'), 0, 6
    ).map(el => el.className.trim()).forEach((klass) => {
      expect(klass).to.equal('inactive');
    });

    // 01.02.2015 is Sunday and it is the selected day.
    expect(
      this.componentElement.querySelectorAll('tbody td')[6].className.trim()
    ).to.equal('selected');

    // Last Sunday is 01.03.2015.
    expect(
      [].slice.call(
        this.componentElement.querySelectorAll('tbody td')
      ).pop().className.trim()
    ).to.equal('inactive');

    // All other days are active.
    [].slice.call(
      this.componentElement.querySelectorAll('tbody td'), 7, 32
    ).map(el => el.className.trim()).forEach((klass) => {
      expect(klass).to.equal('');
    });
  });
});
