'use strict';

import React from 'react';
import { expect } from 'chai';
import { shallow } from 'enzyme';

import ResultsLineups from '../../../components/results/results-lineups.jsx';
import ResultsLineup from '../../../components/results/results-lineup.jsx';


const defaultProps = {
  dateIsToday: false,
  lineups: [
    {
      id: 1,
      sport: 'nba',
      players: [],
      entries: [],
    },
    {
      id: 2,
      sport: 'nba',
      players: [],
      entries: [],
    }
  ],
};

describe("ResultsLineups Component", function() {

  function renderComponent(props = defaultProps) {
    return shallow(<ResultsLineups {...props} />);
  }

  it('should render all expected children', () => {
    const wrapper = renderComponent();
    expect(wrapper.find('.results-page--lineups')).to.have.length(1);
    expect(wrapper.find(ResultsLineup)).to.have.length(2);
  });
});
