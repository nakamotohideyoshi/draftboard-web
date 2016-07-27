import React from 'react';
import sinon from 'sinon';
import { expect } from 'chai';
import { mount } from 'enzyme';
import merge from 'lodash/merge';
import storeUpcomingContestsFix from '../../../fixtures/json/store-upcoming-contests.js';
import ContestListRow from '../../../components/contest-list/contest-list-row.jsx';
import DraftButton from '../../../components/contest-list/draft-button.jsx';
import EnterContestButton from '../../../components/contest-list/enter-contest-button.jsx';


const defaultTestProps = {
  draftGroupsWithLineups: [],
  enterContest: () => true,
  focusedContest: {},
  focusedLineup: {},
  highlighted: false,
  isEntered: false,
  lineupsInfo: {},
  contest: storeUpcomingContestsFix.allContests[
    Object.keys(storeUpcomingContestsFix.allContests)[0]
  ],
  setFocusedContest: () => true,
  entrySkillLevels: {},
};


describe('<ContestListRow /> Component', () => {
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
    const props = merge(
      {}, defaultTestProps, { setFocusedContest: sinon.spy() }
    );
    wrapper = renderComponent(props);
    wrapper.find(ContestListRow).simulate('click');
    // Expect method to be called with the row argument.
    expect(props.setFocusedContest.calledWith(props.contest)).to.equal(true);
    // Expect it to be called only once.
    expect(props.setFocusedContest.callCount).to.equal(1);
  });


  it('should never render a draft button.', () => {
    expect(wrapper.find(DraftButton)).to.have.length(0);
  });


  it('should always render an <enterContestButton />', () => {
    expect(wrapper.find(EnterContestButton)).to.have.length(1);
  });
});
