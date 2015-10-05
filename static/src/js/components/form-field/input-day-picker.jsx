'use strict';

var React = require('react');

var moment = require('moment');


/**
 * Input field that when clicked, opens calendar beneath
 */
var InputDayPicker = React.createClass({

  /**
   * Prop types needed for the InputDayPicker element
   * @type {Object}
   * onDaySelected: function calback, that is to be executed when date is selected
   * placeHolder: placeholder to be putted in the input field by default
   */
  propTypes: {
    onDaySelected: React.PropTypes.func.isRequired,
    placeholder: React.PropTypes.string.isRequired
  },

  getInitialState: function() {
    var today = new Date();
    return {
      value: '',
      month: today,
      showCalendar: false
    };
  },

  /**
  * Overwrite the input field change event use this in case
  * when you want to let user select date directly from the input
  */
  handleInputChange: function(e) {
    e.preventDefault();
  },

  showCalendar: function() {
    this.setState({showCalendar: true});
  },

  hideCalendar: function() {
    this.setState({showCalendar: false});
  },

  /**
   * when date is selected, process it and delegate upwards to the onDaySelected prop func
   */
  handleDayClick: function(e, day) {
    this.setState({
      value: moment(day).format("L"),
      showCalendar: false
    }, this.props.onDaySelected(moment(day)));
  },

  /**
   * position the calendar right below the input field
   */
  updateCalendarStyles: function () {
    var calendarStyles = {};

    if (this.state.showCalendar) {
      calendarStyles = {'display': 'block'};
    } else {
      calendarStyles = {'display': 'none'};
    }

    if ('input' in this.refs) {
      calendarStyles['position'] = 'absolute'
      calendarStyles['height'] = '250px';
      calendarStyles['width'] = '250px';
      calendarStyles['border'] = '1px solid black';
      calendarStyles['top'] = '40px';
      calendarStyles['z-index'] = '500px';
      calendarStyles['background'] = '#fff';
      // this.refs.input.offsetLeft only gets tricky and is browser incompatible
      calendarStyles['left'] = this.refs.input.offsetParent.offsetLeft - 75 + 'px';
    }

    return calendarStyles;
  },

  render: function() {

    var calendarStyles = this.updateCalendarStyles();

    return (
      <span className="input-day-picker">

        <span className="input-symbol-number">
          <input
            className='date-picker'
            ref='input'
            type='text'
            value={this.state.value}
            placeholder={this.props.placeholder}
            onChange={this.handleInputChange}
            onFocus={this.showCalendar} />
            { this.state.showCalendar &&
              <label className="calendar-input-label">{this.props.placeholder}</label>
            }
        </span>

        <span style={calendarStyles}></span>

          { this.state.showCalendar &&
            <div id="daypicker-backdrop" onClick={this.hideCalendar}></div>
          }
      </span>
    );
  }
});


module.exports = InputDayPicker;
