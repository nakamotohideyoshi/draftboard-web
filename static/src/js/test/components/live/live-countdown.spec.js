import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import LiveCountdown from '../../../components/live/live-countdown.jsx';
import CountdownClock from '../../../components/site/countdown-clock';


describe('<LiveCountdown /> Component', () => {
  const renderComponent = (props) => mount(<LiveCountdown {...props} />);
  let wrapper;

  const defaultTestProps = {
    lineup: {
      id: 1,
      draftGroup: 3,
      contests: [2],
      name: 'Curry\'s Chicken',
      start: '2020-10-15T23:00:00Z',
      sport: 'nba',
    },
  };

  beforeEach(() => {
    wrapper = renderComponent(defaultTestProps);
  });

  afterEach(() => {
    document.body.innerHTML = '';
  });

  it('should render countdown clock', () => {
    expect(wrapper.find(CountdownClock)).to.have.length(1);
  });

  it('should have valid lineup edit URL', () => {
    expect(wrapper.find('a.live-countdown__action').get(0).href)
      .to.equal('http://localhost/draft/3/lineup/1/edit/');
  });
});
