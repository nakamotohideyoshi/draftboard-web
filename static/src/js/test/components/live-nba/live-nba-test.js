'use strict';

require('../../test-dom')();
var React = require('react');
var ReactDOM = require('react-dom');
var LiveNBA = require('../../../components/live-nba/live-nba.jsx');
var expect = require('chai').expect;


// note that for this component we only need to check that it renders, as all of its subcomponents are tested separately
describe('LiveNBA Component', function() {

  it('should render a <div>', function() {
    var self = this;

    // Render the component into our fake jsdom element.
    this.sectionComponent = ReactDOM.render(
      <LiveNBA />,
      document.body.appendChild(document.createElement('div')),
      function() {
        // Once it has been rendered, grab it from the DOM.
        var element = ReactDOM.findDOMNode(this);
        expect(element.tagName).to.equal('DIV');
      }
    );
  });

});
