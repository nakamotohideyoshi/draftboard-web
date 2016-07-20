require('../../test-dom')();
import React from 'react';
import ReactDOM from 'react-dom';
import ReactTestUtils from 'react-addons-test-utils';
import ResultsDaysSlider from '../../../components/results/results-days-slider.jsx';
import sinon from 'sinon';
import { expect } from 'chai';

const utils = require('../../../lib/utils');

let selectedDate = null;
const defaultProps = {
  year: 2015,
  month: 1,
  day: 1,
  onSelectDate(year, month, day) {
    selectedDate = [year, month, day];
  }
};

describe("ResultsDaysSlider Component", function() {

  beforeEach(function(done) {
    var self = this;
    selectedDate = null;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.renderComponent = (callback, props = defaultProps) => {
      this.component = ReactDOM.render(
        React.createElement(ResultsDaysSlider, props),
        this.targetElement,
        function() {
          // Once it has been rendered...
          // Grab it from the DOM.
          self.componentElement = ReactDOM.findDOMNode(this);
          callback();
        }
      );
    };

    done();
  });

  afterEach(function() {
    document.body.innerHTML = '';
  });

  it('should render all days for provided month', function(done) {
    this.renderComponent(() => {
      const items = [].slice.apply(this.componentElement.querySelectorAll('.item'));

      expect(this.componentElement.tagName).to.equal('DIV');
      expect(items.length).to.equal(28);
      expect(items[0].className).to.equal("item selected");

      const weekDaysNames = items.map((elm) => elm.textContent.slice(0, 3)).join(',');
      expect(weekDaysNames).to.equal(
        'SUN,MON,TUE,WED,THU,FRI,SAT,SUN,MON,TUE,WED,THU,FRI,SAT,SUN,MON,TUE,WED,THU,FRI,SAT,SUN,MON,TUE,WED,THU,FRI,SAT'
      );

      done();
    });
  });

  it('should scroll to initially provided date', function(done) {
    this.renderComponent(() => {
      expect(this.componentElement.tagName).to.equal('DIV');

      expect(
        this.componentElement.querySelectorAll('.item')[11].className
      ).to.equal("item selected");

      setTimeout(() => {
        expect(this.component.scrollItem).to.equal(11);

        done();
      }, 10);
    }, {
      year: 2015,
      month: 1,
      day: 12,
      onSelectDate(year, month, day) {
        selectedDate = [year, month, day];
      }
    });
  });

  it('should scroll left/right provided date', function(done) {
    this.renderComponent(() => {
      expect(this.componentElement.tagName).to.equal('DIV');

      expect(
        this.componentElement.querySelectorAll('.item')[11].className
      ).to.equal("item selected");

      expect(this.component.scrollItem).to.equal(11);

      ReactTestUtils.Simulate.click(
        this.componentElement.querySelector('.arrow-right')
      );

      setImmediate(() => {
        expect(this.component.scrollItem).to.equal(12);

        ReactTestUtils.Simulate.click(
          this.componentElement.querySelector('.arrow-left')
        );

        setImmediate(() => {
          expect(this.component.scrollItem).to.equal(11);
          done();
        });
      });
    }, {
      day: 12,
      month: 1,
      year: 2015,
      onSelectDate(year, month, day) {
        selectedDate = [year, month, day];
      }
    });
  });


  it('should be able to select a date', function() {
    this.renderComponent(() => {
      expect(this.componentElement.tagName).to.equal('DIV');

      expect(
        this.componentElement.querySelectorAll('.item')[0].className
      ).to.equal("item selected");

      ReactTestUtils.Simulate.click(
        this.componentElement.querySelectorAll('.item')[5]
      );

      expect(selectedDate.toString()).to.equal([2015, 1, 6].toString());
    });
  });

  it('should not be able to select a future date', function(done) {
    const date = new Date(2016, 3, 12);
    const stub = sinon.stub(utils, "dateNow", () => date);
    const today = new Date(utils.dateNow());

    this.renderComponent(() => {
      expect(this.componentElement.tagName).to.equal('DIV');

      expect(
        this.componentElement.querySelectorAll('.item')[today.getDate() - 1].className
      ).to.equal("item selected");

      expect(
        this.componentElement.querySelectorAll('.item')[today.getDate()].className
      ).to.equal("item future");

      ReactTestUtils.Simulate.click(
        this.componentElement.querySelectorAll('.item')[today.getDate() - 1]
      );

      expect(selectedDate.toString()).to.equal([
        today.getFullYear(),
        today.getMonth() + 1,
        today.getDate()
      ].toString());

      ReactTestUtils.Simulate.click(
        this.componentElement.querySelectorAll('.item')[today.getDate()]
      );

      expect(selectedDate.toString()).to.equal([
        today.getFullYear(),
        today.getMonth() + 1,
        today.getDate()
      ].toString());

      utils.dateNow.restore();
      done();
    }, {
      day: today.getDate(),
      month: today.getMonth() + 1,
      year: today.getFullYear(),
      onSelectDate(year, month, day) {
        selectedDate = [year, month, day];
      }
    });
  });
});
