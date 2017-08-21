import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';
import Component from '../../../components/draft/draft-player-detail-game-logs';

const defaultTestProps = {
  player: {},
};


describe('<DraftPlayerDetailGameLogs /> Component', () => {
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
    expect(wrapper.find('.player-splits')).to.have.length(1);
  });


  it('should show a table of game log splits if one exists.', () => {
    wrapper = renderComponent(
      { player: {
        sport: 'nfl',
        position: 'QB',
        splitsHistory: [{
          someState: 0,
        }],
      } }
    );

    expect(wrapper.find(Component)).to.have.length(1);
    expect(wrapper.find('table')).to.have.length(1);
  });
});
