'use strict';

import React from 'react';

import DatePicker from '../site/date-picker';


const InputDayPicker = React.createClass({

  /**
   * Prop types needed for the InputDayPicker element
   * @type {Object}
   * onDaySelected: function calback, that is to be executed when date is selected
   * placeHolder: placeholder to be putted in the input field by default
   */
  propTypes: {
    onDaySelected: React.PropTypes.func.isRequired,
    placeholder:   React.PropTypes.string.isRequired
  },

  getInitialState() {
    return {
      date:         new Date,
      showCalendar: false
    };
  },

  /**
   * Overwrite the input field change event use this in case when you
   * want to let user select date directly from the input.
   */
  handleInputChange(e) {
    e.preventDefault();
  },

  handleShowCalendar() {
    this.setState({showCalendar: true});
  },

  /**
   * When date is selected, process it and delegate upwards to the
   * `onDaySelected` prop function.
   */
  handleSelectDate(year, month, day) {
    const selectedDate = new Date(year, month, day);

    this.setState({
      date:         selectedDate,
      showCalendar: false
    });

    this.props.onDaySelected(selectedDate);
  },

  renderSelectedDate() {
    const today    = this.state.date;
    const year     = today.getFullYear();
    const month    = today.getMonth() + 1; // Months are zero-counted.
    const day      = today.getDate();

    return month + '/' + day + '/' + year;
  },

  renderCalendar() {
    if (!this.state.showCalendar) return null;

    const today    = this.state.date;
    const year     = today.getFullYear();
    const month    = today.getMonth();
    const day      = today.getDate();

    return (
      <DatePicker year={year}
                  month={month}
                  day={day}
                  onSelectDate={this.handleSelectDate} />
    );
  },

  render() {
    return (
      <span className="input-day-picker">

        <span className="input-symbol-number">
          <input
            className='date-picker'
            ref='input'
            type='text'
            value={this.renderSelectedDate()}
            placeholder={this.props.placeholder}
            onChange={this.handleInputChange}
            onFocus={this.handleShowCalendar} />
        </span>

        {this.renderCalendar()}
      </span>
    );
  }
});


export default InputDayPicker;
