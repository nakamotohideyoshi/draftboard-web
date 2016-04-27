import React from 'react';
import ReactDOM from 'react-dom';
import DatePicker from '../site/date-picker';
import { stringifyDate } from '../../lib/time.js';


const InputDayPicker = React.createClass({

  /**
   * Prop types needed for the InputDayPicker element
   * @type {Object}
   * onDaySelected: function calback, that is to be executed when date is selected
   * placeHolder: placeholder to be putted in the input field by default
   */
  propTypes: {
    onDaySelected: React.PropTypes.func.isRequired,
    placeholder: React.PropTypes.string.isRequired,
  },

  getInitialState() {
    return {
      date: null,
      showCalendar: false,
    };
  },


  componentWillMount() {
    document.body.addEventListener('click', this.handleHide, false);
  },

  componentWillUnmount() {
    document.body.removeEventListener('click', this.handleHide);
  },

  /**
   * Overwrite the input field change event use this in case when you
   * want to let user select date directly from the input.
   */
  handleInputChange(e) {
    e.preventDefault();
  },

  handleShowCalendar() {
    this.setState({ showCalendar: true });
  },

  handleHide(e) {
    if (ReactDOM.findDOMNode(this).contains(e.target)) return;

    this.setState({ showCalendar: false });
  },


  /**
   * When date is selected, process it and delegate upwards to the
   * `onDaySelected` prop function.
   */
  handleSelectDate(year, month, day) {
    const selectedDate = new Date(year, month, day);

    this.setState({
      date: selectedDate,
      showCalendar: false,
    });

    this.props.onDaySelected(selectedDate);
  },

  renderSelectedDate() {
    if (this.state.date) {
      const today = this.state.date;
      return stringifyDate(today, '/');
    }

    return '';
  },

  renderCalendar() {
    if (!this.state.showCalendar) return null;

    const today = this.state.date || new Date;
    const year = today.getFullYear();
    const month = today.getMonth();
    const day = today.getDate();

    return (
      <DatePicker
        year={year}
        month={month}
        day={day}
        onSelectDate={this.handleSelectDate}
      />
    );
  },

  renderLabel() {
    if (!this.state.showCalendar) return null;

    return (
      <label className="calendar-input-label">{this.props.placeholder}</label>
    );
  },

  render() {
    return (
      <span className="cmp-input-date-picker">
        <span className="input-symbol-number">
          <input
            className="date-picker-input"
            ref="input"
            type="text"
            value={this.renderSelectedDate()}
            placeholder={this.props.placeholder}
            onChange={this.handleInputChange}
            onFocus={this.handleShowCalendar}
          />
        </span>
        {this.renderLabel()}
        {this.renderCalendar()}
      </span>
    );
  },
});


module.exports = InputDayPicker;
