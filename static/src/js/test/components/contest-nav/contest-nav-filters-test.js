'use strict';

require('../../test-dom')();
const React = require('react');
const ReactDOM = require('react-dom');
const ContestNavFilters = require('../../../components/contest-nav/contest-nav-filters.jsx');
const expect = require('chai').expect;

const defaultProps = {
  selected: "$$$A$$$",
  options: [
    {
      option: "$$$A$$$",
      type: "##1##",
      key: null,
      count: "1"
    } , {
      option: "$$$B$$$",
      type: "##1##",
      key: null,
      count: "2"
    }],
  onChangeSelection: (() => {})
};

function render(props, callback) {
    const targetElement = document.body.appendChild(document.createElement('div'));
    const component = ReactDOM.render(
      React.createElement(ContestNavFilters, props),
      targetElement, function() {
        setTimeout(() => {
          callback(component, ReactDOM.findDOMNode(this));
        });
    });
}

describe("ContestNavFilters Component", function() {

  afterEach(function() {
    document.body.innerHTML = '';
  });

  it('should render a div tag', function() {
    render(defaultProps, (component, domElement) => {
      expect(domElement.tagName).to.equal('DIV');
    });
  });

  it('should render a selected option', function() {
    render(defaultProps, (component, domElement) => {
      const elm = domElement.querySelectorAll('.select-list--selected');

      expect(elm.length).to.equal(1);
      expect(elm[0].innerHTML).to.equal(defaultProps.selected);
    });
  });

  it('should show/hide menu options', function() {
    render(defaultProps, (component, domElement) => {
      const elm = (() => {
        return domElement.querySelectorAll('.select-list--options.visible');
      });

      expect(elm().length).to.equal(0);

      component.handleMenuShow();
      expect(elm().length).to.equal(1);

      component.handleMenuLeave();
      expect(elm().length).to.equal(0);
    });
  });

  it('should select first option if not selected', function() {
    let {options, onChangeSelection} = defaultProps;
    let selected = null;
    let props = {selected, options, onChangeSelection};

    render(props, (component, domElement) => {
      const elm = domElement.querySelectorAll('.select-list--selected');

      expect(elm.length).to.equal(1);
      setTimeout(() => {
        expect(elm[0].innerHTML).to.equal(props.options[0].option);
      }, 200);
    });
  });

});
