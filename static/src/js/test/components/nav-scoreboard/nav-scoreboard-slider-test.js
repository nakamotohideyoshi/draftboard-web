// "use strict";

require('../../test-dom')();

import React from 'react';
import ReactDOM from 'react-dom';
import ReactTestUtils from 'react-addons-test-utils';
import NavScoreboardSlider from "../../../components/nav-scoreboard/nav-scoreboard-slider.jsx";
import { expect } from 'chai';

// TODO: Find a way to test scrolling. Currently JSDOM doesn't support
//       advanced DOM properties used in the component.

describe('NavScoreboardMenu Component', function() {

  beforeEach(function() {
    var self = this;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
  });

  it("should not be scrollable without children", function(done) {
    ReactDOM.render(
      <NavScoreboardSlider />,
      this.targetElement,
      function() {
        const element = ReactDOM.findDOMNode(this);
        expect(element.tagName).to.equal('DIV');
        expect(element.querySelectorAll('.slider-content.not-scrollable').length).to.equal(1);
        done();
      }
    );
  });
});
