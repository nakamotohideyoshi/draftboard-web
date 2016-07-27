'use strict'

import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import { LiveStandingsPane } from '../../../components/live/live-standings-pane';

const defaultProps = {
  actions: {},
  changePathAndMode() {},
  contest: {
    id: 2,
    potentialWinnings: {
      amount: 2,
      percent: 2
    },
    playersOwnership: {
      all: [],
    },
    lineupsUsernames: {}
  },
  openOnStart: true,
  rankedLineups: [2, 3],
  watching: {},
  contestId: 2,
  owned: [
    {
      id: 1,
      name: 'Kobe Bryant',
      team: 'LAL',
      points: 72,
      position: 'pg',
      iamge: '',
      progress: 100
    },
    {
      id: 2,
      name: 'Kobe Bryant',
      team: 'LAL',
      points: 12,
      position: 'c',
      iamge: '',
      progress: 30
    }
  ],
  lineups: {
    3: {
      id: 3,
      rank: 3,
      name: 'villy17',
      points: 72,
      earnings: '$100',
      progress: 74,
      timeRemaining: { decimal: 0.5 },
      potentialWinnings: 2.123123,
    },
    2: {
      id: 2,
      rank: 2,
      name: 'villy18',
      points: 71,
      earnings: '$90',
      progress: 31,
      timeRemaining: { decimal: 0.5 },
      potentialWinnings: 2.123123,
    }
  }
}

describe("LiveStandingsPane Component", function() {

  function renderComponent(props = defaultProps) {
    return mount(<LiveStandingsPane {...props}/>);
  }


  it('should render', function() {
    const wrapper = renderComponent();
    expect(wrapper.find('.live-standings-pane')).to.have.length(1);
  })

  it('should should be able to switch tabs', function() {
    const wrapper = renderComponent();

    expect(wrapper.find('.standings-list')).to.have.length(1);
    expect(wrapper.find('.ownership-list')).to.have.length(0);

    wrapper
      .find('.live-standings-pane__header')
      .find('.menu')
      .find('.title')
      .not('.active')
      .simulate('click');

    expect(wrapper.find('.standings-list')).to.have.length(0);
    expect(wrapper.find('.ownership-list')).to.have.length(1);

    wrapper
      .find('.live-standings-pane__header')
      .find('.menu')
      .find('.title')
      .not('.active')
      .simulate('click');

    expect(wrapper.find('.standings-list')).to.have.length(1);
    expect(wrapper.find('.ownership-list')).to.have.length(0);
  });

  it('should should be able to work with pages', function(done) {
    const wrapper = renderComponent();

    expect(wrapper.find('.lineup')).to.have.length(2);

    wrapper.setState({ perPage: 1 });
    expect(wrapper.instance().getMaxPage()).to.equal(2);

    setTimeout(() => {
      expect(wrapper.find('.lineup')).to.have.length(1);
      expect(wrapper.find('.lineup--place').text().trim()).to.equal('2');
      expect(wrapper.instance().state.page).to.equal(1);

      wrapper.find('.arrow-right').simulate('click');
      expect(wrapper.instance().state.page).to.equal(2);
      expect(wrapper.find('.lineup--place').text().trim()).to.equal('3');

      wrapper.find('.arrow-left').simulate('click');
      expect(wrapper.find('.lineup--place').text().trim()).to.equal('2');
      expect(wrapper.instance().state.page).to.equal(1);

      done();
    }, 10);
  });
})
