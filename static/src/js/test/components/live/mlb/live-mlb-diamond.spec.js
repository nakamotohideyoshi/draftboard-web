import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import LiveMLBDiamond from '../../../../components/live/mlb/live-mlb-diamond.jsx';


/**
 * Tests for LiveMLBDiamond
 * - currently no support in jsdom to handle svgs nor their children, so there are two scenarios untested atm:
 *   github issue here https://github.com/airbnb/enzyme/issues/375
 *   - should render fill differently if a player in my lineup is on base
 *   - should render fill differently if a player in the opposing lineup is on base
 */
describe('<LiveMLBDiamond /> Component', () => {
  const renderComponent = (props) => mount(<LiveMLBDiamond {...props} />);

  afterEach(() => {
    document.body.innerHTML = '';
  });

  it('should render an svg', () => {
    const wrapper = renderComponent({});

    expect(wrapper.find('svg')).to.have.length(1);
  });
});
