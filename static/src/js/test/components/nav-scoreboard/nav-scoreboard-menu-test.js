// "use strict";

require('../../test-dom')();

import React from 'react';
import ReactDOM from 'react-dom';
import ReactTestUtils from 'react-addons-test-utils';
import NavScoreboardMenu from "../../../components/nav-scoreboard/nav-scoreboard-menu.jsx";
import { expect } from 'chai';

describe('NavScoreboardMenu Component', function() {

  beforeEach(function(done) {
    var self = this;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.component = ReactDOM.render(
      <NavScoreboardMenu />,
      this.targetElement,
      function() {
        // Once it has been rendered...
        // Grab it from the DOM.
        self.element = ReactDOM.findDOMNode(this);
        done();
      }
    );
  });

  it("should render a div tag", function() {
    expect(this.element.tagName).to.equal('DIV');
  });

  it("should toogle on click", function() {
    expect(this.targetElement.querySelectorAll('.mobile-forum-hamburger.closed').length).to.equal(0);
    expect(this.targetElement.querySelectorAll('.mobile-forum-hamburger:not(.closed)').length).to.equal(1);

    ReactTestUtils.Simulate.click(
      this.targetElement.querySelector('.mobile-forum-hamburger')
    );

    expect(this.targetElement.querySelectorAll('.mobile-forum-hamburger.closed').length).to.equal(1);
    expect(this.targetElement.querySelectorAll('.mobile-forum-hamburger:not(.closed)').length).to.equal(0);

    ReactTestUtils.Simulate.click(
      this.targetElement.querySelector('.mobile-forum-hamburger')
    );

    expect(this.targetElement.querySelectorAll('.mobile-forum-hamburger.closed').length).to.equal(0);
    expect(this.targetElement.querySelectorAll('.mobile-forum-hamburger:not(.closed)').length).to.equal(1);
  });
});
