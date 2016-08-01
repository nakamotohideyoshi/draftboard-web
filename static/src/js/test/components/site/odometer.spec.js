import React from 'react';
import { assert } from 'chai';
import { mount } from 'enzyme';

import Odometer from '../../../components/site/odometer.jsx';


describe('<Odometer /> Component', () => {
  const renderComponent = (props) => mount(<Odometer {...props} />);

  afterEach(() => {
    document.body.innerHTML = '';
  });

  it('should initialize Odometer plugin within React component', () => {
    const props = {
      value: 0,
    };

    const wrapper = renderComponent(props);

    assert.equal('odometer' in wrapper.node, true);
  });
});
