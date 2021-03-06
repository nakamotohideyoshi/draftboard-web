import React from 'react';
import sinon from 'sinon';
import { expect } from 'chai';
import { mount } from 'enzyme';

const utils = require('../../../lib/utils');
import ResultsDaysSlider from '../../../components/results/results-days-slider.jsx';

let selectedDate = null;
const defaultProps = {
  year: 2015,
  month: 2,
  day: 1,
  onSelectDate(year, month, day) {
    selectedDate = [year, month, day];
  },
};

describe('ResultsDaysSlider Component', () => {
  const renderComponent = (props = defaultProps) => mount(<ResultsDaysSlider {...props} />);

  it('should render all days for provided month', () => {
    const wrapper = renderComponent();
    const items = wrapper.find('.item');

    expect(wrapper.find('.results-days-slider')).to.have.length(1);

    expect(items).to.have.length(28);
    expect(items.first().hasClass('selected')).to.equal(true);

    const weekDaysNames = items.map((elm) => elm.text().slice(0, 3)).join(',');
    expect(weekDaysNames).to.equal(
      'SUN,MON,TUE,WED,THU,FRI,SAT,SUN,MON,TUE,WED,THU,FRI,SAT,SUN,MON,TUE,WED,THU,FRI,SAT,SUN,MON,TUE,WED,THU,FRI,SAT'
    );
  });

  it('should scroll to initially provided date', () => {
    const wrapper = renderComponent({
      year: 2015,
      month: 1,
      day: 12,
      onSelectDate(year, month, day) {
        selectedDate = [year, month, day];
      },
    });

    expect(wrapper.find('.item').at(11).hasClass('selected')).to.equal(true);
  });

  it('should be able to select a date', () => {
    const wrapper = renderComponent();

    expect(wrapper.find('.item').at(0).hasClass('selected')).to.equal(true);
    wrapper.find('.item').at(5).simulate('click');
    expect(selectedDate.toString()).to.equal([2015, 2, 6].toString());
  });

  it('should not be able to select a future date', () => {
    const date = new Date(2016, 3, 12);
    sinon.stub(utils, 'dateNow', () => date);
    const today = new Date(utils.dateNow());
    const wrapper = renderComponent({
      day: today.getDate(),
      month: today.getMonth() + 1,
      year: today.getFullYear(),
      onSelectDate(year, month, day) {
        selectedDate = [year, month, day];
      },
    });

    expect(
      wrapper.find('.item').at(today.getDate() - 1).hasClass('selected')
    ).to.equal(true);
    expect(
      wrapper.find('.item').at(today.getDate()).hasClass('future')
    ).to.equal(true);

    wrapper.find('.item').at(today.getDate() - 1).simulate('click');
    expect(selectedDate.toString()).to.equal([
      today.getFullYear(),
      today.getMonth() + 1,
      today.getDate(),
    ].toString());

    wrapper.find('.item').at(today.getDate()).simulate('click');
    expect(selectedDate.toString()).to.equal([
      today.getFullYear(),
      today.getMonth() + 1,
      today.getDate(),
    ].toString());

    utils.dateNow.restore();
  });
});
