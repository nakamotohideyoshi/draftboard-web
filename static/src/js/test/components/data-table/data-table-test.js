'use strict';

require('../../test-dom')();
var React = require('react/addons');
var DataTable = require('../../../components/data-table/data-table.jsx');
var fixtures = require('../../../fixtures/contests')[0].fixtures();
var expect = require('chai').expect;


describe('DataTable Component', function() {

  beforeEach(function(done) {
    var self = this;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.dataTableComponent = React.render(
      <DataTable data={fixtures} />,
      this.targetElement,
      function() {
        // Once it has been rendered, grab it from the DOM.
        self.dataTableElement = this.getDOMNode();
        done();
      }
    );
  });


  afterEach(function() {
    document.body.innerHTML = '';
  });


  it('should render a <table>', function() {
    expect(this.dataTableElement.tagName).to.equal('TABLE');
  });


  it('should render a <thead>', function() {
    expect(
      this.dataTableElement.querySelectorAll('thead').length
    ).to.equal(1);
  });


  it('should render a <tbody>', function() {
    expect(
      this.dataTableElement.querySelectorAll('tbody').length
    ).to.equal(1);
  });


  it("should render all of the contests as <tr>'s in a <tbody>", function() {
    expect(document.querySelectorAll('tbody tr').length).to.equal(fixtures.length);
  });

});
