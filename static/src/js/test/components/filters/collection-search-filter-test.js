'use strict';

require('../../test-dom')();
var React = require('react');
import ReactDOM from 'react-dom';
var Component = require('../../../components/filters/collection-search-filter.jsx');
var expect = require('chai').expect;
var ReactTestUtils = require('react-addons-test-utils');


describe('CollectionSearchFilter Component', function() {

  beforeEach(function(done) {
    var self = this;
    var onUpdate = function() {};

    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.component = ReactDOM.render(
      <Component
        filterProperty='name'
        filterName='test'
        onUpdate={onUpdate}
      />,
      this.targetElement,
      function() {
        // Once it has been rendered...
        // Grab it from the DOM.
        self.domElement = ReactDOM.findDOMNode(this);
        done();
      }
    );
  });


  afterEach(function() {
    // Remove component from the DOM and empty the DOM for good measure.
    document.body.innerHTML = '';
  });


  it('should render the search input field', function() {
    expect(this.domElement.querySelectorAll('.cmp-collection-search-filter__input').length).to.equal(1);
    expect(this.domElement.querySelector('.cmp-collection-search-filter__input').tagName).to.equal('INPUT');
  });

  //
  // it('should case-insensitively filter a row based on the state.match', function() {
  //   var testRow = {'name': 'the TeSt_qEery-exists!'};
  //   var self = this;
  //
  //   this.component.setState({
  //     match: 'test_qeery'
  //   }, function() {
  //     expect(self.component.filter(testRow)).to.equal(true);
  //   });
  //
  //   this.component.setState({
  //     match: 'no_match_should_be_found'
  //   }, function() {
  //     expect(self.component.filter(testRow)).to.equal(false);
  //   });
  // });


  // it("should add an 'active' className when expanded", function() {
  //   // make sure it's not expanded at first.
  //   expect(this.component.state.isExpanded).to.equal(false);
  //   // after the expand method is called..
  //   this.component.showSearchField();
  //   // check if the state changed...
  //   expect(this.component.state.isExpanded).to.equal(true);
  //   // and the class was added.
  //   expect(ReactDOM.findDOMNode(this.component).className).to.contain('cmp-collection-search-filter--active');
  // });


  it("should show the search field when clicked", function() {
    // Click the element.
    ReactTestUtils.Simulate.click(ReactDOM.findDOMNode(this.component));
    // ensure the active class was added.
    expect(ReactDOM.findDOMNode(this.component).className).to.contain('cmp-collection-search-filter--active');
  });

});
