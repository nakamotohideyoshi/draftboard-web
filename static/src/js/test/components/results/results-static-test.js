require('../../test-dom')();
import moment from 'moment';
import React from 'react';
import ReactDOM from 'react-dom';
import ReactTestUtils from 'react-addons-test-utils';
import ResultsStatic from '../../../components/results/results-static.jsx';
import { expect } from 'chai';
import sinon from 'sinon';

const utils = require('../../../lib/utils');

let selectedDate = null;
const defaultProps = {
  params: {
    year: 2015,
    month: 1,
    day: 1,
  },

  results: {},

  date: {
    year: 2015,
    month: 1,
    day: 1,
    dateIsToday: false,
    formattedDate: '01-01-2015'
  },

  onSelectDate(year, month, day) {
    selectedDate = [year, month, day];
  },

  resultsWithLive: {
    lineups: [],
    overall: {
      winnings: '12',
      possible: '12',
      buyins: '12',
      entries: 12,
      contests: 12,
    },
  },
};

describe("ResultsStatic Component", function() {

  beforeEach(function(done) {
    var self = this;
    selectedDate = null;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.renderComponent = (callback, props = defaultProps) => {
      this.component = ReactDOM.render(
        React.createElement(ResultsStatic, props),
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

  it('should render with provided props', function(done) {
    this.renderComponent(() => {
      expect(this.componentElement.tagName).to.equal('DIV');
      done();
    });
  });

  it('should select current day if not date provided and it is after 10AM', function(done) {
    const date = new Date(2016, 3, 12, 12);
    const stub = sinon.stub(utils, "dateNow", () => date);
    const today = new Date(utils.dateNow());

    this.renderComponent(() => {
      expect(this.componentElement.tagName).to.equal('DIV');

      const today = moment(utils.dateNow());

      expect(selectedDate.join()).to.equal([
        parseInt(today.format('YYYY'), 10),
        parseInt(today.format('M'), 10),
        parseInt(today.format('D'), 10)
      ].join());

      utils.dateNow.restore();
      done();
    }, Object.assign(
      {},
      defaultProps,
      {params: {}}
    ));
  });

  it('should select previous day if not date provided and it is before 10AM', function(done) {
    const date = new Date(2016, 3, 12, 9);
    const stub = sinon.stub(utils, "dateNow", () => date);
    const today = new Date(utils.dateNow());

    this.renderComponent(() => {
      expect(this.componentElement.tagName).to.equal('DIV');

      const today = moment(utils.dateNow());

      today.add(-1, 'days');

      expect(selectedDate.join()).to.equal([
        parseInt(today.format('YYYY'), 10),
        parseInt(today.format('M'), 10),
        parseInt(today.format('D'), 10)
      ].join());

      utils.dateNow.restore();
      done();
    }, Object.assign(
      {},
      defaultProps,
      {params: {}}
    ));
  });
});
