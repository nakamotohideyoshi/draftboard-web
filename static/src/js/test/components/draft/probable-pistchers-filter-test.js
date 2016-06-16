import React from 'react';
import sinon from 'sinon';
import { expect } from 'chai';
import { mount } from 'enzyme';
import ProbablePitchersFilter from '../../../components/draft/probable-pitchers-filter.jsx';
import merge from 'lodash/merge';

const defaultTestProps = {
  enabled: true,
  onUpdate: () => true,
};


describe('<ProbablePitchersFilter /> Component', () => {
  let wrapper;

  function renderComponent(props) {
    return mount(<ProbablePitchersFilter {...props} />);
  }


  beforeEach(() => {
    wrapper = renderComponent(defaultTestProps);
  });


  afterEach(() => {
    document.body.innerHTML = '';
  });


  it('Should render the filter.', () => {
    expect(wrapper.find('.cmp-probable-pitchers-filter')).to.have.length(1);
    expect(wrapper.find('label')).to.have.length(1);
    expect(wrapper.find('input')).to.have.length(1);
    expect(wrapper.find('.text_label')).to.have.length(1);
  });


  it('should run onUpdate() when clicked.', () => {
    // Insert a spy into the props.
    const onUpdateSpy = sinon.spy(() => {});
    wrapper = renderComponent(merge({},
      defaultTestProps,
      { onUpdate: onUpdateSpy })
    );

    // Click the text label.
    wrapper.find('.text_label').simulate('click');
    expect(onUpdateSpy.callCount).to.equal(1);
  });


  it('should show a checked box based on the \'enabled\' prop.', () => {
    // Should default to being checked.
    expect(wrapper.find('.radio-button-list__input').props().checked).to.equal(true);

    // And when the filter is disabled, should not be checked.
    wrapper.setProps({ enabled: false });
    expect(wrapper.find('.radio-button-list__input').props().checked).to.equal(false);
  });
});
