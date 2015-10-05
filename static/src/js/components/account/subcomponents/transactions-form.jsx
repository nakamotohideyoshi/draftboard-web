'use strict';

var React = require('react');
var moment = require('moment');

var InputDayPicker = require('../../form-field/input-day-picker.jsx');


/**
 * All input fields that on the /account/settings/transactions page
 * that are Past Week / Past Month / Options for date selects
 *
 * NOTE:
 * startDaySelected + endDaySelected functions are kind of hacky, should be refactored
 */
var TransactionsForm = React.createClass({

  propTypes: {
    onPeriodSelected: React.PropTypes.func.isRequired
  },

  /**
   * Show calendar inputs if from/to get params in the urls
   * Otherwise hide the calendar inputs
   */
  getInitialState: function() {
    return {
      'showCalendars': false,
      'startDate': null,
      'endDate': null
    };
  },

  /**
   * update component only if showCalendars differ (not when new endDate/startDate is set)
   */
  shouldComponentUpdate: function(nextProps, nextState) {
    return this.state.showCalendars !== nextState.showCalendars;
  },

  /**
   * when Past Week is clicked, set start and end day
   * and trigger getTransaction action with that dates
   */
  pastWeekFetch: function() {
    var today = moment();
    var weekBack = moment().add(-7, 'days');
    this.props.onPeriodSelected(weekBack, today);
  },

  /**
   * when Past Month is clicked, set start and end day
   * and trigger getTransaction action with that dates
   */
  pastMonthFetch: function() {
    var today = moment();
    var monthBack = moment().add(-1, 'months');
    this.props.onPeriodSelected(monthBack, today);
  },

  /**
   * if option Select Dates is clicked, show the calendars (change state.showCalendars)
   */
  selectDates: function() {
    var toggleShow = !this.state.showCalendars;
    this.setState({'showCalendars': toggleShow});
  },

  /**
   * Triggered when start date from calendar is selected
   * If we have end date, fetch transactions (call getTransactions)
   * @param {Object} (required) (moment type object)
   */
  startDaySelected: function(day) {
    this.setState({'startDate': day});
    this.props.onPeriodSelected(day, this.state.endDate);
  },

  /**
   * Triggered when end date from calendar is selected
   * If we have start date, fetch transactions (call getTransactions)
   * @param {Object} (required) (moment type object)
   */
  endDaySelected: function(day) {
    this.setState({'endDate': day});
    this.props.onPeriodSelected(this.state.startDate, day);
  },

  render: function() {
    // we add csrftokken for the "export" option that is POST
    var csrftokken = document.cookie.match(/csrftoken=(.*?)(?:$|;)/)[1];

    return (
      <form
        className="form"
        method="post"
        action="."
      >
        <input type="hidden" name="csrfmiddlewaretoken" value={csrftokken} />

        <fieldset className="form__fieldset__transactions-actions">
          <div className="form-field form-field--inline">
            <span className="past-week-icon" onClick={this.pastWeekFetch}>Past Week</span>
            <span className="past-month-icon" onClick={this.pastMonthFetch}>Past Month</span>
            <span className="select-dates" onClick={this.selectDates}>Select Dates</span>

            { this.state.showCalendars &&
              <span>
                <InputDayPicker
                  onDaySelected={this.startDaySelected}
                  placeholder='Start Day'
                  ref='start-day-input' />
                  -
                <InputDayPicker
                  onDaySelected={this.endDaySelected}
                  placeholder='End Day'
                  ref='end-day-input' />
              </span>
            }
          </div>

          <input type="submit" className="button--medium pull-right" value="Export" />
        </fieldset>
      </form>
    );
  }
});


module.exports = TransactionsForm;
