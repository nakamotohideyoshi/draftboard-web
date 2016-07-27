'use strict';

import React from 'react';
import sinon from 'sinon';
import moment from 'moment';
import { expect } from 'chai';
import { shallow } from 'enzyme';
const utils = require('../../../lib/utils');

import ResultsStatic from '../../../components/results/results-static.jsx';

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

  function renderComponent(props = defaultProps) {
    return shallow(<ResultsStatic {...props} />);
  }

  it('should render with provided props', function() {
    const wrapper = renderComponent();
    expect(wrapper.find('.inner')).to.have.length(1);
  });

  it('should select current day if not date provided and it is after 10AM', function() {
    const date = new Date(2016, 3, 12, 12);
    const stub = sinon.stub(utils, "dateNow", () => date);
    const today = moment(utils.dateNow());
    const wrapper = renderComponent(Object.assign(
      {},
      defaultProps,
      {params: {}}
    ));

    expect(selectedDate.join()).to.equal([
      parseInt(today.format('YYYY'), 10),
      parseInt(today.format('M'), 10),
      parseInt(today.format('D'), 10)
    ].join());

    utils.dateNow.restore();
  });

  it('should select previous day if not date provided and it is before 10AM', function() {
    const date = new Date(2016, 3, 12, 9);
    const stub = sinon.stub(utils, "dateNow", () => date);
    const today = moment(utils.dateNow());
    const wrapper = renderComponent(Object.assign(
      {},
      defaultProps,
      {params: {}}
    ));

    today.add(-1, 'days');
    expect(selectedDate.join()).to.equal([
      parseInt(today.format('YYYY'), 10),
      parseInt(today.format('M'), 10),
      parseInt(today.format('D'), 10)
    ].join());

    utils.dateNow.restore();
  });
});
