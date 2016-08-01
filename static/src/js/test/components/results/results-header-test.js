'use strict';

import React from 'react';
import { expect } from 'chai';
import { shallow } from 'enzyme';

import ResultsHeader from '../../../components/results/results-header.jsx';

describe("ResultsHeader Component", function() {

  function renderComponent() {
    return shallow(<ResultsHeader
                     year={2016}
                     month={1}
                     day={18}
                     onSelectDate={function(){}} />);
  }

  it('should render all expected children', () => {
    const wrapper = renderComponent();
    expect(wrapper.find('.results-page--header')).to.have.length(1);
  });
});
