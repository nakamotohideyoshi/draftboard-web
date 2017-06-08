import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';
import EntrantList from '../../../components/contest-list/entrant-list.jsx';

const defaultTestProps = {
  entrants: [
    { username: 'JuliusSeizure' },
    { username: 'JuliusSeizure' },
    { username: 'JuliusSeizure' },
    { username: 'BreadPitt' },
    { username: 'NapoleonBonerFart' },
  ],
};


describe('<EntrantList /> Component', () => {
  let wrapper;

  function renderComponent(props) {
    return mount(<EntrantList {...props} />);
  }


  beforeEach(() => {
    wrapper = renderComponent(defaultTestProps);
  });


  it('should render.', () => {
    expect(wrapper.find('.cmp-entrant-list')).to.have.length(1);
  });


  it('should have a td for each provided user, showing duplicates.', () => {
    expect(wrapper.find('td.username')).to.have.length(defaultTestProps.entrants.length);
  });


  it('should show an empty element if no entrants are provided.', () => {
    wrapper = renderComponent({});
    expect(wrapper.find('.cmp-entrant-list tr')).to.have.length(0);
    expect(wrapper.text()).to.equal('');
  });
});
