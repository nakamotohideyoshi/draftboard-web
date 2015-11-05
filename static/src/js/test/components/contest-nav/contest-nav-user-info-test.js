'use strict';

require('../../test-dom')();
const React = require('react');
const ReactDOM = require('react-dom');
const ContestNavUserInfo = require('../../../components/contest-nav/contest-nav-user-info.jsx');
const expect = require('chai').expect;

const defaultProps = {
  name: "John",
  balance: "100$"
};

describe("ContestNavUserInfo Component", function() {

  beforeEach(function(done) {
    var self = this;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.contestNavComponent = ReactDOM.render(
      <ContestNavUserInfo
        name={defaultProps.name}
        balance={defaultProps.balance}
        />,
      this.targetElement,
      function() {
        // Once it has been rendered...
        // Grab it from the DOM.
        self.contestNavElement = ReactDOM.findDOMNode(this);
        done();
      }
    );
  });

  afterEach(function() {
    document.body.innerHTML = '';
  });

  it('should render a div tag, name and balance', function() {
    expect(this.contestNavElement.tagName).to.equal('DIV');
    expect(
      this.contestNavElement.querySelectorAll('.name').length
    ).to.equal(1);
    expect(
      this.contestNavElement.querySelector('.name').textContent
    ).to.equal(defaultProps.name);
    expect(
      this.contestNavElement.querySelectorAll('.balance').length
    ).to.equal(1);
    expect(
      this.contestNavElement.querySelector('.balance').firstChild.textContent
    ).to.equal(defaultProps.balance);
  });

});
