import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';
import Component from '../../../components/contest-list/contest-list-header.jsx';


const defaultTestProps = {
  contests: {},
  filters: {
    skillLevelFilter: {},
  },
  updateFilter: () => true,
};


describe('<ContestListHeader /> Component', () => {
  let wrapper;

  function renderComponent(props) {
    return mount(<Component {...props} />);
  }


  beforeEach(() => {
    wrapper = renderComponent(defaultTestProps);
  });


  afterEach(() => {
    document.body.innerHTML = '';
  });


  it('should render a skill level filter.', () => {
    expect(wrapper.find('.contest-list-filter--skill-level')).to.have.length(1);
  });
});
