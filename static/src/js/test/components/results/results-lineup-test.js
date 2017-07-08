import React from 'react';
import { expect,chai } from 'chai';
import { shallow } from 'enzyme';

import { dateNow } from '../../../lib/utils';
import ResultsLineup from '../../../components/results/results-lineup.jsx';

const defaultProps = {
  dateIsToday: false,
  id: 1,
  draftGroupId: 11,
  name: 'test',
  sport: 'nba',
  players: [
    {
      player_id: 2,
      full_name: 'player-name',
      fantasy_points: 100,
      roster_spot: 'asd',
      timeRemaining: new Date,
      player_meta: {
        srid: 'foo',
        team: { alias: 'team-alias' },
      },
      salary: 33,
    },
  ],
  entries: [],
  stats: {
    buyin: 1,
    won: 2,
    entries: 3,
  },
  liveStats: {
    totalBuyin: 100,
    entries: 101,
    fees: 102,
    points: 103,
    potentialWinnings: {},
  },
};



describe('ResultsLineup Component', () => {
  const renderComponent = (props = defaultProps) => shallow(<ResultsLineup {...props} />);
  it('should render all expected children', () => {
    const wrapper = renderComponent();
    expect(wrapper.find('.flip-container')).to.have.length(1);
    expect(wrapper.find('.lineup')).to.have.length(1);
    expect(wrapper.find('.contests')).to.have.length(1);
    expect(wrapper.find('.player')).to.have.length(1);

    const footerItems = wrapper.find('.footer').find('.item');
    expect(footerItems.at(0).text()).to.contain('Won');
    expect(footerItems.at(1).text()).to.contain('Entries');
  });

  it('should render lineup and allow switching to contests', () => {
    const wrapper = renderComponent();
    expect(wrapper.find('.flip-container.hover')).to.have.length(0);
    wrapper.find('.icon-flip.action').simulate('click');
    expect(wrapper.find('.flip-container.hover')).to.have.length(1);
    wrapper.find('.to-lineup').simulate('click');
    expect(wrapper.find('.flip-container.hover')).to.have.length(0);
  });

  it('should render lineup in all supported stages', () => {
    let props;
    let wrapper = null;
    let footerItems = null;

    // Finished
    props = defaultProps;
    wrapper = renderComponent(props).find('.lineup');
    footerItems = wrapper.find('.footer').find('.item');
    expect(footerItems).to.have.length(3);
    expect(footerItems.at(0).text()).to.contain('Won');
    expect(footerItems.at(1).text()).to.contain('Entries');
    expect(wrapper.find('.icon-flip.action')).to.have.length(1);
    expect(wrapper.find('.right-stat-title').text()).to.contain('PTS');

    // Live
    props = Object.assign({}, defaultProps, {
      start: dateNow(),
    });
    delete props.stats;

    wrapper = renderComponent(props).find('.lineup');
    footerItems = wrapper.find('.footer-live').find('.item');
    expect(footerItems.at(0).text()).to.contain('Winning');
    expect(footerItems.at(1).text()).to.contain('Pts');
    expect(wrapper.find('.watch-live')).to.have.length(1);
    expect(wrapper.find('.actions-menu-container .actions').find('li')).to.have.length(1);
    expect(wrapper.find('.right-stat-title').text()).to.contain('PTS');

    // Live footer remains in contests
    wrapper = renderComponent(props).find('.contests');
    footerItems = wrapper.find('.footer-live').find('.item');
    expect(footerItems.at(0).text()).to.contain('Winning');
    expect(footerItems.at(1).text()).to.contain('Pts');
    expect(wrapper.find('.watch-live')).to.have.length(1);

    // Upcoming
    props = Object.assign({}, defaultProps, {
      start: dateNow() + 1000 * 60,
    });
    delete props.stats;

    wrapper = renderComponent(props).find('.lineup');
    footerItems = wrapper.find('.footer-upcoming').find('.item');
    expect(footerItems.at(0).text()).to.contain('Live');
    expect(footerItems.at(1).text()).to.contain('Fees');
    expect(wrapper.find('.actions-menu-container .actions').find('li')).to.have.length(2);
    expect(wrapper.find('.right-stat-title').text()).to.contain('Salary');
  });
});
