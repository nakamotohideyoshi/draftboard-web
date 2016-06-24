import nock from 'nock';
import React from 'react';
import { expect } from 'chai';
import { mount } from 'enzyme';

import LivePMRProgressBar from '../../../components/live/live-pmr-progress-bar.jsx';


/**
 * Tests for LivePMRProgressBar
 * - currently no support in jsdom to handle svgs nor their children, so there are two scenarios untested atm:
 *   - should render linearGradient ids that match fill
 *   - should have proper dimensions within svg
 *   github issue here https://github.com/airbnb/enzyme/issues/375
 */
describe('<LivePMRProgressBar /> Component', () => {
  const renderComponent = (props) => mount(<LivePMRProgressBar {...props} />);

  afterEach(() => {
    document.body.innerHTML = '';
    nock.cleanAll();
  });

  it('should render an svg', () => {
    const props = {
      colors: ['ffffff', 'ffffff', 'ffffff'],
      decimalRemaining: 0.5,
      id: 'foo',
      svgWidth: 50,
    };

    const wrapper = renderComponent(props);

    expect(wrapper.find('svg')).to.have.length(1);
  });

  it('should not render LivePMRProgressBar if decimalRemaining is 0', () => {
    const props = {
      colors: ['ffffff', 'ffffff', 'ffffff'],
      decimalRemaining: 0,
      id: 'foo',
      svgWidth: 50,
    };

    const wrapper = renderComponent(props);

    expect(wrapper.find('svg')).to.have.length(0);
  });

  it('should not render LivePMRProgressBar if strokeDecimal is 0', () => {
    const props = {
      colors: ['ffffff', 'ffffff', 'ffffff'],
      decimalRemaining: 0.5,
      id: 'foo',
      strokeDecimal: 0,
      svgWidth: 50,
    };

    const wrapper = renderComponent(props);

    expect(wrapper.find('svg')).to.have.length(0);
  });
});
