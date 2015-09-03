'use strict';

require('../../test-dom')();
var React = require('react/addons');
var LiveHistoryEvent = require('../../../components/live-nba/live-nba-history-event.jsx');
var expect = require('chai').expect;


// need to repeat the component with different data, so sadly can't use a beforeEach method
describe('LiveHistoryEvent Component', function() {

  it('should render a <div>', function() {
    var self = this;

    this.eventData = {id: 0, "player": "Lebron James", "action": "Rebound", "points": 1, "x": 300, "y": 400};

    // Render the component into our fake jsdom element.
    this.trComponent = React.render(
      <LiveHistoryEvent key={self.eventData.id} event={self.eventData} />,
      document.body.appendChild(document.createElement('div')),
      function() {
        // Once it has been rendered, grab it from the DOM.
        var eventElement = this.getDOMNode();
        expect(eventElement.tagName).to.equal('DIV');
      }
    );

  });

  it('should show a + sign for points', function() {
        var self = this;

    this.eventData = {id: 0, "player": "Lebron James", "action": "Rebound", "points": 1, "x": 300, "y": 400};

    // Render the component into our fake jsdom element.
    this.trComponent = React.render(
      <LiveHistoryEvent key={self.eventData.id} event={self.eventData} />,
      document.body.appendChild(document.createElement('div')),
      function() {
        // Once it has been rendered, grab it from the DOM.
        var eventElement = this.getDOMNode();
        expect(eventElement.querySelectorAll('.live-history-event__points')[0].innerHTML).to.equal('+1');
      }
    );

  });

  it('should show a - sign for points', function() {
    var self = this;

    this.eventData = {id: 0, "player": "Lebron James", "action": "Rebound", "points": -14, "x": 300, "y": 400};

    // Render the component into our fake jsdom element.
    this.trComponent = React.render(
      <LiveHistoryEvent key={self.eventData.id} event={self.eventData} />,
      document.body.appendChild(document.createElement('div')),
      function() {
        // Once it has been rendered, grab it from the DOM.
        var eventElement = this.getDOMNode();
        expect(eventElement.querySelectorAll('.live-history-event__points')[0].innerHTML).to.equal('-14');
      }
    );

  });

});
