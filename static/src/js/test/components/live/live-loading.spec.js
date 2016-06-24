import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import LiveLoading from '../../../components/live/live-loading.jsx';


describe('<LiveLoading /> Component', () => {
  const renderComponent = (props) => mount(<LiveLoading {...props} />);

  afterEach(() => {
    document.body.innerHTML = '';
  });

  it('should render div', () => {
    const testProps = {
      isContestPools: false,
    };
    const wrapper = renderComponent(testProps);

    expect(wrapper.find('.live-loading')).to.have.length(1);
  });

  it('should render message about contest pools when included', () => {
    const testProps = {
      isContestPools: true,
    };
    const wrapper = renderComponent(testProps);

    expect(wrapper.find('.live-loading__contest-pools')).to.have.length(1);
  });
});
