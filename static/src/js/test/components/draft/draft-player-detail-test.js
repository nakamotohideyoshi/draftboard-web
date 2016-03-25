import React from 'react';
import sinon from 'sinon';
import { expect } from 'chai';
import { mount } from 'enzyme';
import { merge as _merge } from 'lodash';
import FocusedPlayerSelectorData from '../../../fixtures/json/focused-player-selector.js';
import DraftPlayerDetail from '../../../components/draft/draft-player-detail.jsx';


const defaultTestProps = {
  draftPlayer: () => true,
  unDraftPlayer: () => true,
  player: FocusedPlayerSelectorData,
};


describe('<DraftPlayerDetail /> Component', () => {
  let wrapper;


  function renderComponent(props) {
    return mount(<DraftPlayerDetail {...props} />);
  }


  // beforeEach(() => {
  //   wrapper = renderComponent(defaultTestProps);
  // });


  it('should render.', () => {
    wrapper = renderComponent(defaultTestProps);
    expect(wrapper.find('.draft-player-detail')).to.have.length(1);
  });


  it('should run the provided methods for draft + undraft clicks.', () => {
    const props = _merge(
      {}, defaultTestProps, {
        draftPlayer: sinon.spy(),
        unDraftPlayer: sinon.spy(),
      }
    );
    wrapper = renderComponent(props);
    const instance = wrapper.instance();
    // Click the draft button.
    wrapper.find('.draft-button').simulate('click');
    expect(instance.props.draftPlayer.callCount).to.equal(1);

    // Set the props to fake the player actually being drafted.
    wrapper.setProps({
      player: Object.assign(
        {},
        props.player,
        { drafted: true }),
    });

    // Click the 'undraft' button.
    wrapper.find('.draft-button.remove').simulate('click');
    expect(instance.props.unDraftPlayer.callCount).to.equal(1);
  });
});
