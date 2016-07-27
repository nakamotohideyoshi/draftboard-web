import React from 'react';
import merge from 'lodash/merge';
import { expect } from 'chai';
import { mount } from 'enzyme';
import EnterContestButton from '../../../components/contest-list/enter-contest-button.jsx';
import storeUpcomingLineupsFix from '../../../fixtures/json/store-upcoming-lineups';
import storeUpcomingContestsFix from '../../../fixtures/json/store-upcoming-contests';
import UpcomingLineupsInfoSelectorFix from
  '../../../fixtures/json/upcoming-lineups-info-selector';


const defaultTestProps = {
  contest: storeUpcomingContestsFix.allContests[
    Object.keys(storeUpcomingContestsFix.allContests)[0]
  ],
  lineup: storeUpcomingLineupsFix.lineups[0],
  lineupsInfo: UpcomingLineupsInfoSelectorFix,
  onEnterClick: () => true,
  onEnterSuccess: () => true,
  onEnterFail: () => true,
  entrySkillLevels: {},
};


describe('<EnterContestButton /> Component', () => {
  let wrapper;

  function renderComponent(props) {
    return mount(<EnterContestButton {...props} />);
  }

  beforeEach(() => {
    wrapper = renderComponent(defaultTestProps);
  });


  it('should render a disabled button if contest has started.', () => {
    wrapper.setState({ hasContestStarted: true });
    expect(wrapper.find('.button.button--disabled')).to.have.length(1);
    // Make sure that it's only rendering 1 .button.
    expect(wrapper.find('.button')).to.have.length(1);
  });


  it('should render an "enter contest" button if the lineup is able to be entered.', () => {
    wrapper.setState({ hasContestStarted: false });
    // Make the button think that the lineup is able to be entered into the contest.
    wrapper.setProps(merge({}, defaultTestProps, {
      lineup: { draft_group: 666 },
      contest: { draft_group: 666 },
    }));

    // Make sure that it's only rendering the 'enter contest' button.
    expect(wrapper.find('.button.enter-contest-button')).to.have.length(1);
    // Make sure that it's only rendering 1 .button.
    expect(wrapper.find('.button')).to.have.length(1);
  });


  it('should now check if the user can enter a contest of this skill level', () => {
    // First set up a situation where we have an entery into a 'rookie' contest, and
    // this contest is 'rookie' also.
    wrapper.setProps({
      entrySkillLevels: {
        nfl: 'rookie',
      },
      contest: {
        id: 1662,
        name: '$100 NFL 10-Man Tourney',
        sport: 'nfl',
        skill_level: {
          name: 'rookie',
        },
      },
    });

    expect(wrapper.instance().matchesCurrentSkillLevel(wrapper.instance().props.contest)).to.equal(true);

    // Now let's pretend we have a 'veteran' entry, while this one is still 'rookie'.
    wrapper.setProps({
      entrySkillLevels: {
        nfl: 'veteran',
      },
    });

    expect(wrapper.instance().matchesCurrentSkillLevel(wrapper.instance().props.contest)).to.equal(false);
  });
});
