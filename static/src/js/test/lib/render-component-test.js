'use strict';

require('../test-dom')();
var React = require('react');
var renderComponent = require('../../lib/render-component');
var expect = require('chai').expect;


describe('RenderComponent', function() {

  beforeEach(function() {
    document.body.innerHTML = '';

    // Create a dummy component to render.
    var componentClass = React.createClass({
      getInitialState: function(){
        return {};
      },
      render: function(){
        return <div className="should-exist">test</div>;
      }
    });

    this.component = React.createElement(componentClass);
  });


  afterEach(function() {
    // Remove all of the nodes we created.
    document.body.innerHTML = '';
  });


  it('should render a single component', function() {
    // Create a div to be rendered to.
    var div = global.document.createElement('div');
    div.className = 'test_element';
    global.document.body.appendChild(div);

    // Render the component.
    renderComponent(this.component, '.test_element');

    expect(global.document.querySelectorAll('.should-exist').length).to.equal(1);
  });


  it('should render multiple components', function() {
    // Create a div to be rendered to.
    var div = global.document.createElement('div');
    div.className = 'test_element';
    global.document.body.appendChild(div);

    // Make another.
    var div2 = global.document.createElement('div');
    div2.className = 'test_element';
    global.document.body.appendChild(div2);

    // And one more.
    var div3 = global.document.createElement('div');
    div3.className = 'test_element';
    global.document.body.appendChild(div3);

    // Render the 3 components.
    renderComponent(this.component, '.test_element');

    expect(global.document.querySelectorAll('.should-exist').length).to.equal(3);
  });

});
