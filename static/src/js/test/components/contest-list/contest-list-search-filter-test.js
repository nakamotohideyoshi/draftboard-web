'use strict';

require('../../test-dom')();
var React = require('react/addons');
var ContestListSearchFilterComponent = require(
  '../../../components/contest-list/contest-list-search-filter.jsx');
var expect = require('chai').expect;


describe('ContestListSearchFilterComponent Component', function() {

  beforeEach(function(done) {
    var self = this;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.searchFilterComponent = React.render(
      <ContestListSearchFilterComponent
        className="contest-list-filter--contest-type"
        filterName="contestSearchFilter"
        property='name'
        match=''
      />,
      this.targetElement,
      function() {
        // Once it has been rendered...
        // Grab it from the DOM.
        self.searchFilterElement = this.getDOMNode();
        done();
      }
    );
  });


  afterEach(function() {
    // Remove component from the DOM and empty the DOM for good measure.
    document.body.innerHTML = '';
  });


  it('should render the search input field', function() {
    expect(this.searchFilterElement.querySelectorAll('.cmp-contest-list-search-filter__input').length).to.equal(1);
    expect(this.searchFilterElement.querySelector('.cmp-contest-list-search-filter__input').tagName).to.equal('INPUT');
  });


  it('should case-insensitively filter a row based on the state.match', function() {
    var testRow = {'name': 'the TeSt_qEery-exists!'};
    var self = this;

    this.searchFilterComponent.setState({
      match: 'test_qeery'
    }, function() {
      expect(self.searchFilterComponent.filter(testRow)).to.equal(true);
    });

    this.searchFilterComponent.setState({
      match: 'no_match_should_be_found'
    }, function() {
      expect(self.searchFilterComponent.filter(testRow)).to.equal(false);
    });
  });


  it("should add an 'active' className when expanded", function() {
    // make sure it's not expanded at first.
    expect(this.searchFilterComponent.state.isExpanded).to.equal(false);
    // after the expand method is called..
    this.searchFilterComponent.showSearchField();
    // check if the state changed...
    expect(this.searchFilterComponent.state.isExpanded).to.equal(true);
    // and the class was added.
    expect(this.searchFilterComponent.getDOMNode().className).to.contain('cmp-contest-list-search-filter--active');
  });


  it("should show the search field when clicked", function() {
    // Click the element.
    React.addons.TestUtils.Simulate.click(this.searchFilterComponent.getDOMNode());
    // ensure the active class was added.
    expect(this.searchFilterComponent.getDOMNode().className).to.contain('cmp-contest-list-search-filter--active');
  });

});
