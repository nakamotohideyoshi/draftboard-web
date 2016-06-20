import React from 'react';
import sinon from 'sinon';
import { expect } from 'chai';
import { mount } from 'enzyme';
import PlayerPositionFilter from '../../../components/draft/player-position-filter.jsx';
import CollectionMatchFilter from '../../../components/filters/collection-match-filter.jsx';
// import merge from 'lodash/merge';

const defaultTestProps = {
  handleFilterChange: () => true,
  positions: [],
  newLineup: [],
  activeFilter: {},
};


// TODO: More testing on <PlayerPositionFilter />
describe('<PlayerPositionFilter /> Component', () => {
  let wrapper;

  function renderComponent(props) {
    return mount(<PlayerPositionFilter {...props} />);
  }


  beforeEach(() => {
    wrapper = renderComponent(defaultTestProps);
  });


  afterEach(() => {
    document.body.innerHTML = '';
  });


  it('Should render the filter.', () => {
    expect(wrapper.find('.cmp-player-position-filter')).to.have.length(1);
    expect(wrapper.find(CollectionMatchFilter)).to.have.length(1);
    expect(wrapper.find('.collection-filter--player-type')).to.have.length(1);
  });
});
