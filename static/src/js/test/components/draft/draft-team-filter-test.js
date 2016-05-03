import React from 'react';
import sinon from 'sinon';
import { expect } from 'chai';
import { mount } from 'enzyme';
import { merge as _merge } from 'lodash';
import DraftTeamFilter from '../../../components/draft/draft-team-filter.jsx';
import sportsStore from '../../../fixtures/json/store-sports.js';
import activeDraftGroupBoxScoresSelectorFix from '../../../fixtures/json/active-draft-group-box-scores-selector.js';


// const defaultTestProps = {
//   onFilterChange: () => true,
//   teams: sportsStore,
//   boxScores: activeDraftGroupBoxScoresSelectorFix,
//   isVisible: true,
// };

// describe('<DraftTeamFilter /> Component', () => {
//   let wrapper;

//   function renderComponent(props) {
//     return mount(<DraftTeamFilter {...props} />);
//   }

//   beforeEach(() => {
//     wrapper = renderComponent(defaultTestProps);
//   });


//   it('should render nothing when isVisible is false', () => {
//     const props = _merge(
//       {}, defaultTestProps, {
//         isVisible: false,
//       }
//     );

//     wrapper = renderComponent(props);
//     expect(wrapper.find('.cmp-draft-team-filter')).to.have.length(0);
//   });


//   it('should render filters when isVisible is true', () => {
//     expect(wrapper.find('.cmp-draft-team-filter')).to.have.length(1);
//   });


//   it('should know if a team is selected with isTeamSelected().', () => {
//     const instance = wrapper.instance();
//     const teams = [321, 123, 5, 6, 7, 'hello'];
//     expect(instance.isTeamSelected(teams, 6)).to.equal(true);
//     expect(instance.isTeamSelected(teams, 'hello')).to.equal(true);
//     expect(instance.isTeamSelected(teams, null)).to.equal(false);
//     expect(instance.isTeamSelected([], 8)).to.equal(false);
//     expect(instance.isTeamSelected(teams, 8)).to.equal(false);
//   });


//   it('handleGameClick() should run when a game is clicked.', () => {
//     // Due to react's auto-binding, we have to spy the __reactAutoBindMap method.
//     // http://stackoverflow.com/a/27280563
//     const clickSpy = sinon.spy(DraftTeamFilter.prototype.__reactAutoBindMap, 'handleGameClick');
//     wrapper = renderComponent(defaultTestProps);

//     // The 0th .game is the 'all games' tile, we want the first actual game.
//     wrapper.find('.game').at(1).simulate('click');
//     expect(clickSpy.callCount).to.equal(1);
//   });


//   it('handleAllClick() should run when "all games" is clicked.', () => {
//     const clickSpy = sinon.spy(DraftTeamFilter.prototype.__reactAutoBindMap, 'handleAllClick');
//     wrapper = renderComponent(defaultTestProps);

//     wrapper.find('.game').at(0).simulate('click');
//     expect(clickSpy.callCount).to.equal(1);
//   });
// });
