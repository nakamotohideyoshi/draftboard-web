// 'use strict';

// require('../../test-dom')();
// var React = require('react');
// var ReactDOM = require('react-dom');
// var expect = require('chai').expect;
// var request = require("superagent");
// var config = require('../../../fixtures/live-nba-store-config.js');
// var LiveNBALineup = require('../../../components/live-nba/live-nba-lineup.jsx');


// describe('LiveNBALineup Component', function() {

//   before(function() {
//     // var self = this;
//     // this.timeout(10000);

//     this.superagentMock = require('superagent-mock')(request, config);

//     this.LiveNBAStore = require('../../../stores/live-nba-store');
//     this.LiveNBAActions = require('../../../actions/live-nba-actions');

//     this.LiveNBAActions.loadContestLineups(1);
//     this.LiveNBAActions.loadDraftGroup(1);
//     this.LiveNBAActions.loadDraftGroupFantasyPoints(1);
//     this.LiveNBAActions.loadLineup(2, 'mine');
//     this.LiveNBAActions.loadLineup(3, 'opponent');

//     // Object.observe(LiveNBAStore.data, function(changes) {
//     //   console.log('changed', changes);
//     //   console.log(changes.object.initAjaxCompleted);

//     //   if (changes.name === 'initLoaded' && changes.object.initLoaded === true) {
//     //     done();
//     //   }

//     // });
//   });

//   after(function() {
//     this.superagentMock.unset();

//     // reset data
//     this.LiveNBAStore.resetData();
//   });

//   it('should render a <div>', function() {
//     var self = this;

//     // Render the component into our fake jsdom element.
//     this.sectionComponent = ReactDOM.render(
//       <LiveNBALineup />,
//       document.body.appendChild(document.createElement('div')),
//       function() {
//         // Once it has been rendered, grab it from the DOM.
//         var element = ReactDOM.findDOMNode(this);
//         expect(element.tagName).to.equal('DIV');
//       }
//     );
//   });


//   // TODO change this to be async
//   it('should render players by default', function() {
//     var self = this;

//     // Render the component into our fake jsdom element.
//     this.sectionComponent = ReactDOM.render(
//       <LiveNBALineup />,
//       document.body.appendChild(document.createElement('div')),
//       function() {
//         // Once it has been rendered, grab it from the DOM.
//         var element = ReactDOM.findDOMNode(this);
//         expect(element.querySelectorAll('.live-lineup-player').length).to.be.above(0);
//       }
//     );
//   });


//   // TODO change this to be async
//   it('should adjust class if whichSide is `me`', function() {
//     var self = this;

//     // Render the component into our fake jsdom element.
//     this.sectionComponent = ReactDOM.render(
//       <LiveNBALineup whichSide='me' />,
//       document.body.appendChild(document.createElement('div')),
//       function() {
//         // Once it has been rendered, grab it from the DOM.
//         var element = ReactDOM.findDOMNode(this);
//         expect(element.getAttribute('class')).to.contain('live-lineup--me');
//       }
//     );
//   });
// });
