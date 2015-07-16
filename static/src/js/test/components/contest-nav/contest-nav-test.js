'use strict';

require('../../test-dom')();
var React = require('react/addons');
var expect = require('chai').expect;
var ContestNav = require('../../../components/contest-nav/contest-nav.jsx');


describe('ContesetNav Component', function() {
  beforeEach(function(done) {
    var self = this;
    document.body.innerHTML = '';
    this.targetElement = document.body.appendChild(document.createElement('div'));

    React.render(
      <ContestNav />,
      this.targetElement,
      function() {
        self.contestNavComponent = this;
        self.ContestNavElement = this.getDOMNode();
        done();
      }
    );
  });


  afterEach(function() {
    document.body.innerHTML = '';
  });


  it('should render a div tag and a list component', function() {
    console.log(this.contestNavComponent);
    expect(this.ContestNavElement.tagName).to.equal('DIV');
    expect(
      this.ContestNavElement.querySelectorAll('.cmp-contest-nav--contests-list').length
    ).to.equal(1);
  });

});
