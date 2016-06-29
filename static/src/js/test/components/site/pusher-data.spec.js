import assert from 'assert';
import React from 'react';
import { mount } from 'enzyme';

import { PusherData } from '../../../components/site/pusher-data';


describe('<PusherData /> Component', () => {
  let wrapper;
  // mocking propTypes
  const defaultTestProps = {
    actions: {},
    addEventAndStartQueue: () => true,
    draftGroupTiming: {},
    fetchSportIfNeeded: () => true,
    hasRelatedInfo: false,
    myLineup: {},
    params: {},
    relevantGamesPlayers: {},
    sportsSelector: {},
    updatePlayerStats: () => true,
    watching: {},
  };
  const renderComponent = (props) => mount(<PusherData {...props} />);

  beforeEach(() => {
    wrapper = renderComponent(defaultTestProps);
  });

  afterEach(() => {
    document.body.innerHTML = '';
  });

  it('should render nothing', () => {
    assert.equal(wrapper.component.props.context, null);
  });

  // TODO tests pusher-data.spec.js
  // should bind boxscores when data is loaded
  // should change pusher bindings when sport changes
});
