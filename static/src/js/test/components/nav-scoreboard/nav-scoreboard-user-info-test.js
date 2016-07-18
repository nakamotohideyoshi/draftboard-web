'use strict';

require('../../test-dom')();
const React = require('react');
const ReactDOM = require('react-dom');
import NavScoreboardUserInfo from '../../../components/nav-scoreboard/nav-scoreboard-user-info.jsx';
const expect = require('chai').expect;

const defaultProps = {
  name: 'John',
  cashBalance: {
    amount: 100,
  },
};

describe('NavScoreboardUserInfo Component', function () {

  beforeEach(function (done) {
    var self = this;
    document.body.innerHTML = '';
    // The DOM element that the component will be rendered to.
    this.targetElement = document.body.appendChild(document.createElement('div'));
    // Render the component into our fake jsdom element.
    this.component = ReactDOM.render(
      <NavScoreboardUserInfo
        name={defaultProps.name}
        balance={defaultProps.cashBalance.amount}
    />,
      this.targetElement,
      function () {
        // Once it has been rendered...
        // Grab it from the DOM.
        self.element = ReactDOM.findDOMNode(this);
        done();
      }
    );
  });

  afterEach(function () {
    document.body.innerHTML = '';
  });

  it('should render a div tag, name and balance', function () {
    expect(this.element.tagName).to.equal('DIV');
    expect(
      this.element.querySelectorAll('.name').length
    ).to.equal(1);
    expect(
      this.element.querySelector('.name').textContent
    ).to.equal(defaultProps.name);
    expect(
      this.element.querySelectorAll('.balance').length
    ).to.equal(1);
    expect(
      this.element.querySelector('.balance').firstChild.textContent
    ).to.equal(`$${defaultProps.cashBalance.amount}.00`);
  });
});
