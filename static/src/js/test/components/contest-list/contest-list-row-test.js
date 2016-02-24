import React from 'react';
import sinon from 'sinon';
import { expect } from 'chai';
import { mount } from 'enzyme';
import { merge as _merge } from 'lodash';
import ContestListRow from '../../../components/contest-list/contest-list-row.jsx';

const defaultTestProps = {
  draftGroupsWithLineups: [],
  enterContest: () => true,
  focusedContest: {},
  focusedLineup: {},
  highlighted: false,
  isEntered: false,
  lineupsInfo: {},
  row: {
    id: 8,
    name: 'player name',
  },
  setFocusedContest: () => true,
};


describe('ContestListRow Component', () => {
  let wrapper;


  function renderComponent(props) {
    // We have to render a table + tbody or else react gets mad.
    return mount(<table><tbody><ContestListRow {...props} /></tbody></table>);
  }


  beforeEach(() => {
    // Render the component before each test. If needed we can re-render with
    // different props.
    wrapper = renderComponent(defaultTestProps);
  });


  it('should render a <tr>.', () => {
    expect(wrapper.find(ContestListRow)).to.have.length(1);
  });


  it('should run props.setFocusedContest(props.row) when clicked.', () => {
    // Update the default props with a spy function.
    const props = _merge(
      {}, defaultTestProps, { setFocusedContest: sinon.spy() }
    );
    wrapper = renderComponent(props);
    wrapper.find(ContestListRow).simulate('click');
    // Expect method to be called with the row argument.
    expect(props.setFocusedContest.calledWith(props.row)).to.equal(true);
    // Expect it to be called only once.
    expect(props.setFocusedContest.callCount).to.equal(1);
  });


  it('should always render a draft button.', () => {
    expect(wrapper.find('.draft-button')).to.have.length(1);
  });
});
