'use strict';

require('../../test-dom')();
var React = require('react/addons');
var Td = require('../../../components/data-table/data-table-td.jsx');
var expect = require('chai').expect;


describe('DataTableTd Component', function() {

  beforeEach(function(done) {
    var self = this;

    this.props = {cellName: 'the-name_of5the+cell', cellData: 'html to be displayed'};

    this.tdComponent = React.render(
      <Td cellName={this.props.cellName} cellData={this.props.cellData} />,
      document.body.appendChild(document.createElement('table')),
      function() {
        self.tdElement = this.getDOMNode();
        done();
      }
    );
  });


  afterEach(function () {
    document.body.innerHTML = '';
  });


  it('should render a <td>', function() {
    expect(document.querySelectorAll('td').length).to.equal(1);
    expect(this.tdElement.tagName).to.equal('TD');
  });


  it('should have a className of cell-<props.cellName>', function() {
    expect(this.tdElement.className).to.equal('cell-' + this.props.cellName);
  });


  it('should display the provided content', function() {
    expect(this.tdElement.innerHTML).to.equal(this.props.cellData);
  });

});
