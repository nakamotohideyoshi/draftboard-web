import React from 'react';
// import sinon from 'sinon';
// import merge from 'lodash/merge';
import { expect } from 'chai';
import { mount } from 'enzyme';
import DraftNewLineupCardPlayer from '../../../components/draft/draft-new-lineup-card-player.jsx';
import DraftNewLineupCard from '../../../components/draft/draft-new-lineup-card.jsx';
import StoreCreateLineupFix from '../../../fixtures/json/store-create-lineup.js';


const defaultTestProps = {
  lineup: StoreCreateLineupFix.lineup,
  lineupTitle: null,
  lineupCanBeSaved: false,
  isActive: false,
  remainingSalary: 50000,
  avgRemainingPlayerSalary: 6250,
  handleEmtpySlotClick: () => true,
  handlePlayerClick: () => true,
  errorMessage: null,
  sport: 'nba',
  saveLineup: () => true,
  removePlayer: () => true,
};


describe('<DraftNewLineupCard /> Component', () => {
  let wrapper;

  function renderComponent(props) {
    return mount(<DraftNewLineupCard {...props} />);
  }

  beforeEach(() => {
    wrapper = renderComponent(defaultTestProps);
  });


  it('should render.', () => {
    expect(wrapper.find('.cmp-lineup-card--new')).to.have.length(1);
  });


  it('should render a card for each player in the lineup', () => {
    expect(wrapper.find(DraftNewLineupCardPlayer)).to.have.length(defaultTestProps.lineup.length);
  });


  it('save button should not be enabled until lineupCanBeSaved is true.', () => {
    // The disabled save button should exist.
    expect(wrapper.find('.cmp-lineup-card__save.button--disabled')).to.have.length(1);
    // Set the lineup as 'saveable'.
    wrapper.setProps({ lineupCanBeSaved: true });
    // The disabled save button should be gone.
    expect(wrapper.find('.cmp-lineup-card__save.button--disabled')).to.have.length(0);
    // The enabled save button should exist.
    expect(wrapper.find('.cmp-lineup-card__save')).to.have.length(1);
  });
});
