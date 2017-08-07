import React from 'react';
import { assert } from 'chai';
import { mount } from 'enzyme';
import Component from '../../../components/contest-list/scoring-info';

const defaultTestProps = {
  sport: 'nba',
  isModal: false,
};


describe('<ScoringInfo /> Component', () => {
  let wrapper;

  function renderComponent(props) {
    return mount(<Component {...props} />);
  }


  beforeEach(() => {
    wrapper = renderComponent(defaultTestProps);
  });


  it('should render.', () => {
    assert.lengthOf(
      wrapper.find('.cmp-scoring-info'),
      1,
      'Component is not rendering'
    );
  });


  it('should render TR\'s when a valid sport is provided', () => {
    assert.isAbove(
      wrapper.find('tbody tr').length,
      0,
      'Not rendering table data'
    );
  });

  it('should NOT render TR\'s when an invalid sport is provided', () => {
    wrapper.setProps({ sport: 'invalid sport' });

    assert.lengthOf(
      wrapper.find('tbody tr'),
      0,
      'is rendering invalid table data.'
    );
  });


  it('should render with modal.', () => {
    wrapper.setProps({ isModal: true });
    assert.lengthOf(
      wrapper.find('.score-table'),
      1,
      'Component is not rendering'
    );
  });

  /* tests for modal mode */
  it('should render .score-col-name when a valid sport is provided', () => {
    wrapper.setProps({ isModal: true });
    assert.lengthOf(
      wrapper.find('.score-col'),
      2,
      'Not rendering table data'
    );
  });

  it('should NOT render .score-col-name when an invalid sport is provided', () => {
    wrapper.setProps({ sport: 'invalid sport', isModal: true });

    assert.lengthOf(
      wrapper.find('.score-col-name'),
      0,
      'is rendering invalid table data.'
    );
  });
});
