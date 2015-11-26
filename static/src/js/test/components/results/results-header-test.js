'use strict';

require('../../test-dom')();
const React = require('react');
const ReactDOM = require('react-dom');
const ResultsHeader = require('../../../components/results/results-header.jsx');
const expect = require('chai').expect;

describe("ResultsHeader Component", function() {

  beforeEach(function(done) {
    var self = this;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.component = ReactDOM.render(
      <ResultsHeader><div id="c--tst"></div></ResultsHeader>,
      this.targetElement,
      function() {
        // Once it has been rendered...
        // Grab it from the DOM.
        self.componentElement = ReactDOM.findDOMNode(this);
        done();
      }
    );
  });

  afterEach(function() {
    document.body.innerHTML = '';
  });

  it('should render its children', function() {
    expect(this.componentElement.tagName).to.equal('DIV');

    expect(
      this.componentElement.querySelectorAll('#c--tst').length
    ).to.equal(1);
  });

});
