'use strict';

import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import NavScoreboardFilters from '../../../components/nav-scoreboard/nav-scoreboard-filters.jsx';

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

describe("NavScoreboardFilters Component", function() {

  function renderComponent(props = defaultProps) {
    return mount(<NavScoreboardFilters {...props} />);
  }

  it('should render', function() {
    const wrapper = renderComponent();
    expect(wrapper.find('.cmp-nav-scoreboard--filters')).to.have.length(1);
  });

  it('should render a selected option', function() {
    const wrapper = renderComponent();
    expect(wrapper.find('.cmp-nav-scoreboard--filters')).to.have.length(1);

    const selected = wrapper.find('.select-list--selected');
    expect(selected).to.have.length(1);
    expect(selected.text()).to.equal(defaultProps.selected);
  });

  it('should show/hide menu options', function() {
    const wrapper = renderComponent();

    expect(wrapper.find('.select-list--options.visible')).to.have.length(0);

    wrapper.instance().handleMenuShow();
    expect(wrapper.find('.select-list--options.visible')).to.have.length(1);

    wrapper.instance().handleMenuLeave();
    expect(wrapper.find('.select-list--options.visible')).to.have.length(0);
  });

  it('should select first option if not selected', function(done) {
    const { options } = defaultProps;
    const selected = null;
    const onChangeSelection = (option) => {
      expect(option).to.equal(options[1].option);
      done();
    };

    renderComponent({ selected, options, onChangeSelection });
  });
});
