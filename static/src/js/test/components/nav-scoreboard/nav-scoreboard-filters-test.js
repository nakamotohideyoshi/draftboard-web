'use strict';

require('../../test-dom')();
const React = require('react');
const ReactDOM = require('react-dom');
import NavScoreboardFilters from '../../../components/nav-scoreboard/nav-scoreboard-filters.jsx';
const expect = require('chai').expect;

const defaultProps = {
  selected: "$$$A$$$",
  options: [
    {
      option: "$$$A$$$",
      type: "##1##",
      key: 1,
      count: 1
    } , {
      option: "$$$B$$$",
      type: "##1##",
      key: 2,
      count: 2
    }],
  onChangeSelection: (() => {})
};

function render(props, callback) {
    const targetElement = document.body.appendChild(document.createElement('div'));
    const component = ReactDOM.render(
      React.createElement(NavScoreboardFilters, props),
      targetElement, function() {
        setTimeout(() => {
          callback(component, ReactDOM.findDOMNode(this));
        });
    });
}

describe("NavScoreboardFilters Component", function() {

  afterEach(function() {
    document.body.innerHTML = '';
  });

  it('should render a div tag', function(done) {
    render(defaultProps, (component, domElement) => {
      expect(domElement.tagName).to.equal('DIV');
      done();
    });
  });

  it('should render a selected option', function(done) {
    render(defaultProps, (component, domElement) => {
      const elm = domElement.querySelectorAll('.cmp-nav-scoreboard--filters .select-list--selected');

      expect(elm.length).to.equal(1);
      expect(elm[0].textContent).to.equal(defaultProps.selected);
      done();
    });
  });

  it('should show/hide menu options', function(done) {
    render(defaultProps, (component, domElement) => {
      const elm = (() => {
        return domElement.querySelectorAll('.select-list--options.visible');
      });

      expect(elm().length).to.equal(0);

      component.handleMenuShow();
      expect(elm().length).to.equal(1);

      component.handleMenuLeave();
      expect(elm().length).to.equal(0);
      done();
    });
  });

  it('should select first option if not selected', function(done) {
    const { options } = defaultProps;
    const selected = null;
    const onChangeSelection = (option) => {
      expect(option).to.equal(props.options[0].option)
      done();
    };
    const props = { selected, options, onChangeSelection };

    render(props, (component, domElement) => {});
  });

});
