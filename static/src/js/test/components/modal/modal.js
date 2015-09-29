'use strict';

require('../../test-dom')();
var sinon = require("sinon");
var onCloseSpy = sinon.spy(function() {return;});
var React = require('react/addons');
var Component = require('../../../components/modal/modal.jsx');
var expect = require('chai').expect;


describe('Modal Component', function() {

  var modalContent = 'This is our modal content';
  var component;

  var render = function(done) {
    document.body.innerHTML = '';

    // Render the component into our fake jsdom element.
    component = React.render(
      <Component onClose={onCloseSpy}>
        <div>{modalContent}</div>
      </Component>,
      document.body,
      function() {
        // Once it has been rendered...
        done();
      }
    );
  };


  beforeEach(function(done) {
    render(done);
  });


  afterEach(function(done) {
    // Unmount the component
    React.unmountComponentAtNode(document.body);
    // Remove component from the DOM and empty the DOM for good measure.
    document.body.innerHTML = '';
    /**
     * pushing the render's callback to the next tick of the eventloop (using setTimeout) resulted
     * in a more stable test environment.
     * (http://www.asbjornenge.com/wwc/testing_react_components.html)
     */
    setTimeout(done);
  });


  it('should render a single .cmp-modal element', function() {
    expect(document.querySelectorAll('.cmp-modal').length).to.equal(1);
  });


  it('should render a .cmp-modal element as a child of the body tag', function() {
    expect(document.querySelector('.cmp-modal').parentNode.tagName).to.equal('BODY');
  });


  it('should render child content inside of a .cmp-modal__content element.', function() {
    expect(document.querySelector('.cmp-modal__content div').innerHTML).to.equal(modalContent);
  });


  it('should run the provided onClose prop function when the close button is pressed', function() {
    var closeBtn = React.findDOMNode(component.refs.closeBtn);
    React.addons.TestUtils.Simulate.click(closeBtn);
    sinon.assert.calledOnce(onCloseSpy);
  });

});
