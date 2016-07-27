'use strict';

import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import NavScoreboardStatic from '../../../components/nav-scoreboard/nav-scoreboard-static.jsx';

const { TYPE_SELECT_GAMES, TYPE_SELECT_LINEUPS } = NavScoreboardStatic;

const defaultProps = {
  user: {username: 'fasfas'},
  sportsSelector: {
    types: ['type1'],
    type1: {
      gameIds: [1],
    },
    games: {
      1: {
        sport: 'mlb',
        awayTeamInfo: {alias: '1'},
        homeTeamInfo: {alias: '2'},
      }
    }
  },
  myCurrentLineupsSelector: {},
  cashBalance: '132123',
  isLivePage: 'faf',
};

describe("NavScoreboardStatic Component", function() {

  function renderComponent(props = defaultProps) {
    return mount(<NavScoreboardStatic {...props} />);
  }

  it("should render a div tag, menu, user info, filters, slider and logo", () => {
    const wrapper = renderComponent();

    expect(wrapper.find('.cmp-nav-scoreboard--menu')).to.have.length(1);
    expect(wrapper.find('.cmp-nav-scoreboard--user-info')).to.have.length(1);
    expect(wrapper.find('.cmp-nav-scoreboard--filters')).to.have.length(1);
    expect(wrapper.find('.cmp-nav-scoreboard--slider')).to.have.length(1);
    expect(wrapper.find('.cmp-nav-scoreboard--logo')).to.have.length(1);
  });

  it("should select and render the first filters option", () => {
    const wrapper = renderComponent();
    const cmp = wrapper.instance();

    expect(cmp.state.selectedOption).to.equal(cmp.getSelectOptions()[0].option);

    if (cmp.state.selectedType == TYPE_SELECT_LINEUPS) {
      expect(wrapper.find('.cmp-nav-scoreboard--lineups-list')).to.have.length(1);
    } else if (cmp.state.selectedType == TYPE_SELECT_GAMES) {
      expect(wrapper.find('.cmp-nav-scoreboard--games-list')).to.have.length(1);
    } else {
      new Error("Selected nav-scoreboard filter is not rendered.");
    }
  });

});
