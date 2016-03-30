import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';
import DraftButton from '../../../components/contest-list/draft-button.jsx';

const defaultTestProps = {
  draftGroupId: 666,
  // A time in the future
  disableTime: '2099-03-15T23:00:00Z',
};


describe('<DraftButton /> Component', () => {
  let wrapper;

  function renderComponent(props) {
    return mount(<DraftButton {...props} />);
  }


  beforeEach(() => {
    // Render the component before each test. If needed we can re-render with
    // different props.
    wrapper = renderComponent(defaultTestProps);
  });


  it('should always render some kind of .draft-button element.', () => {
    expect(wrapper.find('.draft-button')).to.have.length(1);
  });


  it('should link to the provided draftgroup page', () => {
    // These are both basically the same.
    expect(wrapper.find('a.draft-button').get(0).href).to.equal('/draft/666/');
    expect(wrapper.find('a[href="/draft/666/"]')).to.have.length(1);
  });


  it('should not show a draft button if the contest has started', () => {
    wrapper = renderComponent({
      draftGroupId: 3,
      // A time in the past
      disableTime: '2009-03-15T23:00:00Z',
    });
    // should not be a link.
    expect(wrapper.find('a')).to.have.length(0);
    // should show a draft-botton-none span.
    expect(wrapper.find('span.draft-button-none')).to.have.length(1);
  });
});
