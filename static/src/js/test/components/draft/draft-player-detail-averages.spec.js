import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';
import Component from '../../../components/draft/draft-player-detail-averages';

const defaultTestProps = {
  player: {},
};


describe('<DraftPlayerDetailAverages /> Component', () => {
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


  it('should render with an empty player prop object.', () => {
    expect(wrapper.find(Component)).to.have.length(1);
    expect(wrapper.find('.player-stats')).to.have.length(1);
  });


  it('should show a list if boxScoreHistory exists.', () => {
    wrapper = renderComponent(
      { player: {
        sport: 'nfl',
        position: 'QB',
        boxScoreHistory: {
          someState: 0,
        },
      } }
    );

    expect(wrapper.find(Component)).to.have.length(1);
    expect(wrapper.find('ul')).to.have.length.above(1);
  });
});
