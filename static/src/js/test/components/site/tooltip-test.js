'use strict';

require('../../test-dom')();
// var sinon = require("sinon");
var React = require('react/addons');
var Tooltip = require('../../../components/site/tooltip.jsx');
var expect = require('chai').expect;


describe('Tooltip Component', function() {

  beforeEach(function(done) {
    var self = this;
    document.body.innerHTML = '';

    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.TooltipComponent = React.render(
      <Tooltip
        isVisible={true}
        position='top'
        additionalClassName='extras'
      />,
      this.targetElement,
      function() {
        // Once it has been rendered...  Grab it from the DOM.
        self.TooltipElement = React.findDOMNode(this);
        done();
      }
    );
  });


  afterEach(function() {
    // Remove component from the DOM and empty the DOM for good measure.
    document.body.innerHTML = '';
  });


  it('should render a .tooltip div', function() {
    expect(document.querySelectorAll('.tooltip').length).to.equal(1);
  });


  it('should have the directional position class', function() {
    expect(document.querySelectorAll('.tooltip--top-arrow').length).to.equal(1);
  });


  // Re-render the thing and make sure it's got the hidden class.
  it('should be hidden able to be hidden with props + show/hide/toggle', function() {
    document.body.innerHTML = '';
    this.targetElement = document.body.appendChild(document.createElement('div'));

    this.TooltipComponent = React.render(
      <Tooltip
        isVisible={false}
      />,
      this.targetElement,
      function() {
        // Is it hidden by default as specified?
        expect(document.querySelectorAll('.tooltip--hidden').length).to.equal(1);

        // test show/hide/toggle
        this.show(function() {
          expect(document.querySelectorAll('.tooltip--hidden').length).to.equal(0);
        });

        this.hide(function() {
          expect(document.querySelectorAll('.tooltip--hidden').length).to.equal(1);
        });

        this.toggle(function() {
          expect(document.querySelectorAll('.tooltip--hidden').length).to.equal(0);
        });

        this.toggle(function() {
          expect(document.querySelectorAll('.tooltip--hidden').length).to.equal(1);
        });
      }
    );
  });

});
