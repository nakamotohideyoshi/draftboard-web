'use strict';

require('../../test-dom')();
const React = require('react');
const ReactDOM = require('react-dom');
const ReactTestUtils = require('react-addons-test-utils');
import ResultsDaysSlider from '../../../components/results/results-days-slider.jsx';
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
      expect(this.componentElement.tagName).to.equal('DIV');
      expect(
        this.componentElement.querySelectorAll('.item').length
      ).to.equal(28);

      expect(
        this.componentElement.querySelectorAll('.item')[0].className
      ).to.equal("item selected");

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
      year:  2015,
      month: 1,
      day:   12,
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

      setTimeout(() => {
        expect(this.component.scrollItem).to.equal(11);

        ReactTestUtils.Simulate.click(
          this.componentElement.querySelector('.arrow-right')
        );

        setTimeout(() => {
          expect(this.component.scrollItem).to.equal(12);

          setTimeout(() => {
            ReactTestUtils.Simulate.click(
              this.componentElement.querySelectorAll('.arrow-left')
            );

            done();
          }, 10);

          setTimeout(() => {
            expect(this.component.scrollItem).to.equal(11);

            done();
          }, 20);
        }, 10);
      }, 10);
    }, {
      year:  2015,
      month: 1,
      day:   12,
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

});
