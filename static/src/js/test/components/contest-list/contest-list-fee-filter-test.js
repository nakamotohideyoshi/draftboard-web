'use strict';

require('../../test-dom')();
var React = require('react/addons');
var ContestListFeeFilterComponent = require(
  '../../../components/contest-list/contest-list-fee-filter.jsx');
var expect = require('chai').expect;
var sinon = require("sinon");
var ContestActions = require("../../../actions/contest-actions");


describe('ContestListFeeFilterComponent Component', function() {

  beforeEach(function(done) {
    var self = this;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.feeFilterComponent = React.render(
      <ContestListFeeFilterComponent
        className="contest-list-filter--contest-fee"
        filterName="contestFeeFilter"
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


  it('should instantiate the noUiSlider plugin', function() {
    expect(this.searchFilterElement.querySelectorAll('.noUi-target').length).to.equal(1);
  });


  it('should filter rows based on a value range', function() {
    var testRow = {
      'buyin': '50.00'
    };

    this.feeFilterComponent.setState({
      match: {
        minVal: 1,
        maxVal: 100
      }
    }, function() {
      expect(this.feeFilterComponent.filter(testRow)).to.equal(true);
    }.bind(this));

    this.feeFilterComponent.setState({
      match: {
        minVal: 51,
        maxVal: 100
      }
    }, function() {
      expect(this.feeFilterComponent.filter(testRow)).to.equal(false);
    }.bind(this));
  });


  it('should alert the ContestStore that something has changed via an action', function() {
    sinon.spy(ContestActions, "filterUpdated");

    this.feeFilterComponent.handleChange({
      match: {
        minVal: 99,
        maxVal: 100
      }
    });

    sinon.assert.calledOnce(ContestActions.filterUpdated);
  });
});
