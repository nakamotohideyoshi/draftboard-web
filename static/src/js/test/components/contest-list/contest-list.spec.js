import React from 'react';
import { mount } from 'enzyme';
import { assert } from 'chai';
import ContestListComponent from '../../../components/contest-list/contest-list';
import ContestListRow from '../../../components/contest-list/contest-list-row';
import UpcomingContestSelectorFix
  from '../../../fixtures/json/selectors-output/contest-pools-selector';

const defaultTestProps = {
  setOrderBy: () => true,
  contests: UpcomingContestSelectorFix,
  draftGroupsWithLineups: [],
  enterContest: () => true,
  focusedContest: {},
  focusedLineup: {},
  hoveredLineupId: undefined,
  lineupsInfo: {},
  setFocusedContest: () => true,
  entrySkillLevels: {},
  isFetchingContestPools: false,
};


describe('ContestList Component', () => {
  let wrapper;

  function renderComponent(props) {
    return mount(<ContestListComponent {...props} />);
  }

  beforeEach(() => {
    wrapper = renderComponent(defaultTestProps);
  });


  it('should render a table tag', () => {
    assert.lengthOf(wrapper.find('table'), 1, 'Table tag is not rendered.');
  });


  // Make sure it's rendiring the skill level filter
  it('should render each contest', () => {
    assert.lengthOf(
      wrapper.find(ContestListRow),
      UpcomingContestSelectorFix.length,
      'skill level filter is not rendered.'
    );
  });
});
