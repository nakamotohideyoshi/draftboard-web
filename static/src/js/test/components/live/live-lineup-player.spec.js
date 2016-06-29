// import React from 'react';
// import { expect } from 'chai';
// import { mount } from 'enzyme';

// import LiveMLBDiamond from '../../../../components/live/mlb/live-mlb-diamond.jsx';
// import LiveLineupPlayer from '../../../../components/live/mlb/live-mlb-lineup-player-watch.jsx';


// /**
//  * Tests for LiveLineupPlayer
//  */
// describe('<LiveLineupPlayer /> Component (mlb)', () => {
//   const renderComponent = (props) => mount(<LiveLineupPlayer {...props} />);

//   const defaultTestProps = {
//     draftGroupStarted: true,
//     eventDescription: {},
//     gameStats: {},
//     isPlaying: false,
//     isRunner: false,
//     playerType: 'pitcher',
//     isWatching: false,
//     multipartEvent: {},
//     openPlayerPane: () => 'openPlayerPane() ran',
//     player: {},
//     playerImagesBaseUrl: '',
//     setWatchingPlayer: () => 'setWatchingPlayer() ran',
//     sport: 'mlb',
//     whichSide: 'mine',
//   };

//   afterEach(() => {
//     document.body.innerHTML = '';
//   });

//   it('should render a li', () => {
//     const wrapper = renderComponent(defaultTestProps);

//     expect(wrapper.find('li.live-lineup-player')).to.have.length(1);
//   });

//   it('should render out modifiers correctly', () => {
//     const wrapper = renderComponent(defaultTestProps);

//     expect(wrapper.find(
//       'li.live-lineup-player state--'
//     )).to.have.length(1);
//   });

//   it('should render properly', () => {
//     const wrapper = renderComponent(defaultTestProps);

//     expect(wrapper.find('.live-mlb-lineup-player-watch__fp').text()).to.equal('3.2');
//     expect(wrapper.find('.live-mlb-lineup-player-watch__name').text()).to.equal('Foo Bar');
//     expect(wrapper.find('.live-mlb-lineup-player-watch__pitch-count').text()).to.equal('3');
//     expect(wrapper.find('.live-mlb-lineup-player-watch__inning-str').text()).to.equal('8th');

//     expect(wrapper.find(LiveMLBDiamond)).to.have.length(1);
//   });
// });
