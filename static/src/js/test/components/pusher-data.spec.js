import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';
import { PusherData } from '../../components/site/pusher-data';

const defaultTestProps = {
  dispatch: () => { console.warn('foo') },
  draftGroupTiming: {},
  hasRelatedInfo: false,
  relevantGamesPlayers: {},
  myLineup: {},
  watching: {},
  params: {},
  sportsSelector: {},
};

describe('<PusherData /> Component', () => {
  let wrapper;

  function renderComponent(props) {
    return mount(<PusherData {...props} />);
  }

  beforeEach(() => {
    wrapper = renderComponent(defaultTestProps);
  });


  it('should render a yes', () => {
    console.warn(wrapper);
  });


  // it('should toggle between form and info states.', () => {
  //   expect(wrapper.find('.info-state')).to.have.length(1);
  //   expect(wrapper.find('.edit-state')).to.have.length(0);
  //   wrapper.setState({ editMode: true });
  //   expect(wrapper.find('.edit-state')).to.have.length(1);
  //   expect(wrapper.find('.info-state')).to.have.length(0);
  // });


  // it('should display each setting type.', () => {
  //   expect(
  //     wrapper.find('li')
  //   ).to.have.length(defaultTestProps.emailNotificationSettings.length);
  //   // Change to edit mode and check for the right number of radio toggles.
  //   wrapper.setState({ editMode: true });
  //   expect(
  //     wrapper.find('input[type="radio"]')
  //   ).to.have.length(defaultTestProps.emailNotificationSettings.length * 2);
  // });
});
