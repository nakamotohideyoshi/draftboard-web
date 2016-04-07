import React from 'react';
// import sinon from 'sinon';
import { expect } from 'chai';
import { mount } from 'enzyme';
// import { merge as _merge } from 'lodash';
import SettingsEmailNotifications from
  '../../../components/account/subcomponents/settings-email-notifications.jsx';
import emailNotificationSettings from
  '../../../fixtures/json/user-settings-email-notifications.js';

const defaultTestProps = {
  user: {},
  errors: [],
  handleSubmit: () => true,
  emailNotificationSettings,
  isUpdatingEmail: false,
  isFetchingEmail: false,
};

describe('<SettingsEmailNotifications /> Component', () => {
  let wrapper;

  function renderComponent(props) {
    return mount(<SettingsEmailNotifications {...props} />);
  }

  beforeEach(() => {
    wrapper = renderComponent(defaultTestProps);
  });


  it('should render a form', () => {
    expect(wrapper.find('.cmp-settings-email-notifications')).to.have.length(1);
  });


  it('should toggle between form and info states.', () => {
    expect(wrapper.find('.info-state')).to.have.length(1);
    expect(wrapper.find('.edit-state')).to.have.length(0);
    wrapper.setState({ editMode: true });
    expect(wrapper.find('.edit-state')).to.have.length(1);
    expect(wrapper.find('.info-state')).to.have.length(0);
  });


  it('should display each setting type.', () => {
    expect(
      wrapper.find('li')
    ).to.have.length(defaultTestProps.emailNotificationSettings.length);
    // Change to edit mode and check for the right number of radio toggles.
    wrapper.setState({ editMode: true });
    expect(
      wrapper.find('input[type="radio"]')
    ).to.have.length(defaultTestProps.emailNotificationSettings.length * 2);
  });
});
