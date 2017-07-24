import nock from 'nock';
import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import PlayerPmrHeadshotComponent from '../../../components/site/PlayerPmrHeadshotComponent.jsx';
import LivePMRProgressBar from '../../../components/live/live-pmr-progress-bar.jsx';


describe('<PlayerPmrHeadshotComponent /> Component', () => {
  const renderComponent = (props) => mount(<PlayerPmrHeadshotComponent {...props} />);

  afterEach(() => {
    document.body.innerHTML = '';
    nock.cleanAll();
  });

  it('should not render LivePMRProgressBar if there is no decimalRemaining', () => {
    const props = {
      decimalRemaining: 0,  // relevant field
      playerSrid: '',
      sport: 'mlb',
      uniquePmrId: 'my-pmr',
      width: 50,
    };

    const wrapper = renderComponent(props);

    expect(wrapper.find(LivePMRProgressBar)).to.have.length(0);
  });

  it('should render default headshot when player headshot does not exist', () => {
    const props = {
      decimalRemaining: 0,
      playerSrid: 'my-player-srid',  // relevant field
      sport: 'mlb',  // relevant field
      uniquePmrId: 'my-pmr',
      width: 50,
    };

    nock('http://localhost/')
      .get('mlb/120/my-player-srid.png')
      .reply(403);

    const wrapper = renderComponent(props);
    // TODO rewrite this for background styles instead of img element
    expect(wrapper.find('span')).to.have.length(1);
  });

  it('should render with normal data', () => {
    const props = {
      colors: ['ffffff', 'ffffff', 'ffffff'],
      decimalRemaining: 0.5,
      modifiers: ['upcoming'],
      playerSrid: 'my-player-srid',
      sport: 'mlb',
      uniquePmrId: 'my-pmr',
      width: 50,
    };

    nock('http://localhost/')
      .get('mlb/120/my-player-srid.png')
      .reply(200);

    const wrapper = renderComponent(props);
    // TODO rewrite this for background styles instead of img element
    // expect(wrapper.find('img.player-pmr-headshot__headshot--default')).to.have.length(0);
    expect(wrapper.find(LivePMRProgressBar)).to.have.length(1);
  });
});
