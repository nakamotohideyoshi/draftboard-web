// "use strict";

// require('../../test-dom')();
// var HamburgerMenu = require("../../../components/site/hamburger-menu");
// var expect = require('chai').expect;


// describe('HamburgerMenu Component', function() {

//   beforeEach(function() {
//     this.body = global.document.querySelector('body');
//     // Reset any body classes and elements
//     this.body.className = '';
//     this.body.innerHTML = '<div class="other-element"></div><div class="nav-main-trigger"><span class="nav-main-trigger__menu"></span><div class="nav-main-trigger__logo"></div></div><nav class="nav-main"></nav>';
//   });

//   it("should return false if no DOM element exists to attach to", function() {
//     this.body.innerHTML = '';

//     var didAttach = HamburgerMenu.attachNavEventHandlers();
//     expect(didAttach).to.equal(false);
//   });

//   it("should return true when nav element exists", function() {
//     HamburgerMenu.removeNavEventHandlers();

//     var didAttach = HamburgerMenu.attachNavEventHandlers();
//     expect(didAttach).to.equal(true);
//   });

//   it("should open and close when trigger is clicked and anything else is clicked", function(done) {
//     HamburgerMenu.removeNavEventHandlers();
//     HamburgerMenu.attachNavEventHandlers();

//     var navTrigger = document.body.querySelectorAll(".nav-main-trigger")[0];

//     // DOM level 3 click event (annoying that we can't just use .click())
//     var click_ev = document.createEvent("MouseEvents");
//     click_ev.initEvent("click", true /* bubble */, true /* cancelable */);

//     document.body.querySelector('.nav-main-trigger').dispatchEvent(click_ev);

//     // need the timeouts due to async connections to stores for the app class state update
//     setTimeout(function() {
//       expect(document.body.className).to.equal(' appstate--nav-main--open');

//       // now close by clicking on the body
//       var click_ev = document.createEvent("MouseEvents");
//       click_ev.initEvent("click", true /* bubble */, true /* cancelable */);
//       document.body.querySelector('.other-element').dispatchEvent(click_ev);

//       setTimeout(function() {
//         expect(document.body.className).to.equal(' ');
//         done();
//       }, 10);

//     }, 10);




//   });
// });
