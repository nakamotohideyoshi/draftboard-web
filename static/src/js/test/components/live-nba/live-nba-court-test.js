'use strict';

require('../../test-dom')();
var React = require('react/addons');
var LiveNBACourt = require('../../../components/live-nba/live-nba-court.jsx');
var LiveNBAStore = require('../../../stores/live-nba-store.js');
var expect = require('chai').expect;


// need to repeat the component with different data, so sadly can't use a beforeEach method
describe('LiveNBACourt Component', function() {

  it('should render a <section>', function() {
    var self = this;

    // Render the component into our fake jsdom element.
    this.sectionComponent = React.render(
      <LiveNBACourt />,
      document.body.appendChild(document.createElement('div')),
      function() {
        // Once it has been rendered, grab it from the DOM.
        var courtElement = this.getDOMNode();
        expect(courtElement.tagName).to.equal('SECTION');
      }
    );
  });


  it("should not render shooters with no history events", function() {
    var self = this;

    // Render the component into our fake jsdom element.
    this.sectionComponent = React.render(
      <LiveNBACourt />,
      document.body.appendChild(document.createElement('div')),
      function() {
        // Once it has been rendered, grab it from the DOM.
        var courtElement = this.getDOMNode();
        expect(courtElement.querySelectorAll('.shooter-position').length).to.equal(0);
      }
    );
  });


  it("should render shooters when history event is pushed", function(done) {
    this.timeout(4000);
    var self = this;

    // Render the component into our fake jsdom element.
    this.sectionComponent = React.render(
      <LiveNBACourt />,
      document.body.appendChild(document.createElement('div')),
      function() {

        LiveNBAStore.onEventReceived('mine', {
          isSuccessful: true,
          id: 6,
          'player': 'df187cd4-4d7d-11e5-885d-feff819cdc9g',
          'action': 'Layup',
          'points': 2,
          'x': 600,
          'y': 200
        });

        var courtElement = this.getDOMNode();

        setTimeout(function () {
          expect(courtElement.querySelectorAll('.shooter-position').length).to.be.above(0);
          done();
        }, 2000);

      }
    );
  });

});
