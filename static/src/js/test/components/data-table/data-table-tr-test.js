'use strict';

require('../../test-dom')();
var React = require('react/addons');
var Tr = require('../../../components/data-table/data-table-tr.jsx');
var expect = require('chai').expect;


describe('DataTableTr Component', function() {

  beforeEach(function(done) {
    var self = this;

    this.rowData = {id: 4, title: 'test', name: 'steve'};

    // Render the component into our fake jsdom element.
    this.trComponent = React.render(
      <Tr row={self.rowData} />,
      document.body.appendChild(document.createElement('table')),
      function() {
        // Once it has been rendered, grab it from the DOM.
        self.trElement = this.getDOMNode();
        done();
      }
    );
  });


  afterEach(function() {
    // React.unmountComponentAtNode(this.targetElement);
    document.body.innerHTML = '';
  });


  it('should render a <tr>', function() {
    expect(this.trElement.tagName).to.equal('TR');
  });


  it('should render a <td> for each cell provided.', function() {
    expect(this.trElement.querySelectorAll('td').length).to.equal(3);
  });


  it('should exclude <td>\'s when a column whitelist is provided.', function() {
    // Clear the dom and render a new element that has a limited set of columns passed to it.
    var self = this;
    document.body.innerHTML = '';
    var columnWhitelist = ['id', 'name'];

    React.render(
      <Tr row={self.rowData} columns={columnWhitelist} />,
      document.body.appendChild(document.createElement('table')),
      function() {
        // Are we only rendering the columns in the whitelist?
        expect(this.getDOMNode().querySelectorAll('td').length).to.equal(columnWhitelist.length);
      }
    );


  });

});
