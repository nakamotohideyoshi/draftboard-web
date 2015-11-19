'use strict';

import React from 'react';

const InputDayPicker = require('../../form-field/input-day-picker.jsx');


const TransactionsForm = React.createClass({

  propTypes: {
    onPeriodSelected: React.PropTypes.func.isRequired
  },

  getInitialState() {
    return {showCalendarInputs: false}
  },

  /**
   * when Past Week is clicked, set start and end day
   * and trigger getTransaction action with that dates
   */
  handlePastWeekFetch() {
    // var today = moment();
    // var weekBack = moment().add(-7, 'days');
    // this.props.onPeriodSelected(weekBack, today);
  },

  handlePastMonthFetch() {
    // var today = moment();
    // var monthBack = moment().add(-1, 'months');
    // this.props.onPeriodSelected(monthBack, today);
  },

  handleSelectDate() {
    const toggler = !this.state.showCalendarInputs;
    this.setState({showCalendarInputs: toggler});
  },

  handleStartDateSelected() {
  },

  handleEndDateSelected() {
  },

  render() {
    return (
      <form
        className="form"
        method="post"
        action="."
      >
        <fieldset className="form__fieldset__transactions-actions">
          <div className="form-field form-field--inline">
            <span className="past-week-icon" onClick={this.handlePastWeekFetch}>Past Week</span>
            <span className="past-month-icon" onClick={this.handlePastMonthFetch}>Past Month</span>
            <span className="select-dates" onClick={this.handleSelectDate}>Select Dates</span>

            { this.state.showCalendarInputs &&
              <span>
                <InputDayPicker
                  onDaySelected={this.handleStartDateSelected}
                  placeholder='Start Day'
                  ref='start-day-input' />
                  -
                <InputDayPicker
                  onDaySelected={this.handleEndDateSelected}
                  placeholder='End Day'
                  ref='end-day-input' />
              </span>
            }
          </div>

          <input
            type="submit"
            className="button--medium pull-right"
            value="Export" />
        </fieldset>
      </form>
    );
  }
});


export default TransactionsForm;
