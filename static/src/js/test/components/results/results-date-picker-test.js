'use strict';

import React from 'react';
import { expect } from 'chai';
import { shallow } from 'enzyme';

import ResultsDatePicker from '../../../components/results/results-date-picker.jsx';
import DatePicker from '../../../components/site/date-picker.jsx';

let selectedDate = null;
const defaultProps = {
  year:  2015,
  month: 1,
  day:   1,
  onSelectDate(year, month, day) {
    selectedDate = [year, month, day];
  }
};

describe("ResultsDatePicker Component", function() {

  function renderComponent(props = defaultProps) {
    return shallow(<ResultsDatePicker {...props} />);
  }

  it('should render all expected children', () => {
    const wrapper = renderComponent();
    expect(wrapper.find(DatePicker)).to.have.length(0);
    wrapper.find('.toggle').simulate('click');
    expect(wrapper.find(DatePicker)).to.have.length(1);
    wrapper.find('.toggle').simulate('click');
    expect(wrapper.find(DatePicker)).to.have.length(0);
  });
});
