'use strict';

import React from 'react';
import { expect } from 'chai';
import { shallow } from 'enzyme';

import ResultsStats from '../../../components/results/results-stats.jsx';

const defaultProps = {
  stats: {
    winnings: "101",
    possible: "512.4",
    buyins:   "359",
    entries:  18,
    contests: 8
  },
};

describe("ResultsStats Component", function() {

  function renderComponent(props = defaultProps) {
    return shallow(<ResultsStats {...props} />);
  }

  it('should render all provided stats', function() {
    const wrapper = renderComponent();
    expect(wrapper.find('.results-page--stats')).to.have.length(1);

    expect(
      wrapper.find('.winnings').find('.value').text().trim()
    ).to.equal('$' + defaultProps.stats.winnings);

    expect(
      wrapper.find('.possible').find('.value').text().trim()
    ).to.equal('$' + defaultProps.stats.possible);

    expect(
      wrapper.find('.buyins').find('.value').text().trim()
    ).to.equal('$' + defaultProps.stats.buyins);

    expect(
      wrapper.find('.entries').find('.value').text().trim()
    ).to.equal(defaultProps.stats.entries.toString());

    expect(
      wrapper.find('.contests').find('.value').text().trim()
    ).to.equal(defaultProps.stats.contests.toString());
  });
});
