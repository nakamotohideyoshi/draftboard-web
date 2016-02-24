import React from 'react';

const InputDayPicker = require('../../form-field/input-day-picker.jsx');


const TransactionsForm = React.createClass({

  propTypes: {
    onPeriodSelected: React.PropTypes.func.isRequired,
  },

  getInitialState() {
    return {
      showCalendarInputs: false,
      startDate: null,
      endDate: null,
    };
  },

  /**
   * when Past Week is clicked, set start and end day
   * and trigger getTransaction action with that dates
   */
  handlePastWeekFetch() {
    this.hideCalendarInputs();
    this.props.onPeriodSelected({ isPeriod: false, days: 7 });
  },

  handlePastMonthFetch() {
    this.hideCalendarInputs();
    // Get a 1 month start + end date.
    const today = new Date();
    const oneMonthAgo = new Date();
    oneMonthAgo.setMonth(today.getMonth() - 1);
    this.props.onPeriodSelected({ isPeriod: true, startDate: oneMonthAgo, endDate: today });
  },

  handleSelectDate() {
    const toggler = !this.state.showCalendarInputs;
    this.setState({ showCalendarInputs: toggler });
  },

  handleStartDateSelected(date) {
    this.setState({ startDate: date });

    if (this.state.endDate) {
      this.props.onPeriodSelected({
        isPeriod: true,
        startDate: date,
        endDate: this.state.endDate,
      });
    }
  },

  handleEndDateSelected(date) {
    this.setState({ endDate: date });

    if (this.state.startDate !== null) {
      this.props.onPeriodSelected({
        isPeriod: true,
        startDate: this.state.startDate,
        endDate: date,
      });
    }
  },

  hideCalendarInputs() {
    this.setState({
      showCalendarInputs: false,
      startDate: null,
      endDate: null,
    });
  },

  render() {
    return (
      <form
        className="form transactions-form"
        method="post"
        action="."
      >
        <fieldset className="form__fieldset__transactions-actions">
          <div className="form-field form-field--inline">
            <span className="past-week-icon" onClick={this.handlePastWeekFetch}>Past Week</span>
            <span className="past-month-icon" onClick={this.handlePastMonthFetch}>Past Month</span>
            <span className="select-dates" onClick={this.handleSelectDate}>Select Dates</span>

            { this.state.showCalendarInputs &&
              <div className="transactions-date-pickers">
                <InputDayPicker
                  onDaySelected={this.handleStartDateSelected}
                  placeholder="Start Day"
                  ref="start-day-input"
                />
                <span>-</span>
                <InputDayPicker
                  onDaySelected={this.handleEndDateSelected}
                  placeholder="End Day"
                  ref="end-day-input"
                />
              </div>
            }

            { false &&
              <div className="transactions-date-pickers">
                <span>
                  <span className="input-symbol-number">
                    <input type="text" />
                  </span>
                </span>
                <span>-</span>
                <span>
                  <span className="input-symbol-number">
                    <input type="text" />
                  </span>
                </span>
              </div>

            }

          </div>

          <input
            type="submit"
            className="button--medium pull-right"
            value="Export"
          />
        </fieldset>
      </form>
    );
  },
});


export default TransactionsForm;
