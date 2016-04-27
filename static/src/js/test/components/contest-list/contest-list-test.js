'use strict';

require('../../test-dom')();
var assert = require('assert');
var React = require('react');
import ReactDOM from 'react-dom';
var ContestListComponent = require('../../../components/contest-list/contest-list.jsx');
// var expect = require('chai').expect;


describe('ContestList Component', function () {

  beforeEach(function (done) {
    var self = this;
    let props = {
      featuredContests: [],
      setOrderBy: function () {return true;}
    };
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.contestListComponent = ReactDOM.render(
      <ContestListComponent {...props} />,
      this.targetElement,
      function () {
        // Once it has been rendered...
        // Grab it from the DOM.
        self.contestListElement = ReactDOM.findDOMNode(this);
        done();
      }
    );
  });


  afterEach(function () {
    // Remove component from the DOM and empty the DOM for good measure.
    //
    // These suckers don't clean up nicely, so ignore this for now.
    // ReactDOM.unmountComponentAtNode(this.targetElement);
    document.body.innerHTML = '';
  });


  it('should render a div tag', function () {
    assert.equal(this.contestListElement.tagName, 'TABLE');
  });


  // Make sure it's rendiring the contest list filters (there will eventually be 3).
  // it('should render the contest type filters', function() {
  //   expect(this.contestListElement.querySelectorAll('.contest-list-filter').length).to.equal(2);
  // });

});
