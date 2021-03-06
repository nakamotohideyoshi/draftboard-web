import React from 'react';
import PureRenderMixin from 'react-addons-pure-render-mixin';

import {
  getDaysForMonth, weekdayNumToName, monthNumToName, daysToWeekView,
} from '../../lib/time.js';
import { isDateInTheFuture } from '../../lib/utils';

const DatePicker = React.createClass({

  propTypes: {
    year: React.PropTypes.number.isRequired,
    month: React.PropTypes.number.isRequired,
    day: React.PropTypes.number.isRequired,
    onSelectDate: React.PropTypes.func.isRequired,
  },

  mixins: [PureRenderMixin],

  getInitialState() {
    const { year, month, day } = this.props;
    return { year, month, day };
  },

  componentWillMount() {
    this.setDate(this.props);
  },

  componentWillReceiveProps(nextProps) {
    this.setDate(nextProps);
  },

  getWeeklyMonthData() {
    const { year, month } = this.state;

    const daysOfTheMonth = getDaysForMonth(year, month);
    const daysByWeeks = daysToWeekView(daysOfTheMonth);

    return daysByWeeks;
  },

  /**
   * Sets the date of the slider. We don't use the date from props
   * because the internal state of the calendar may differ from the
   * actually selected date in props. This function is basically used
   * to copy date information from props to state.
   */
  setDate({ year, month, day }) {
    this.setState({ year, month, day });
  },

  handleSelectDate(year, month, day) {
    this.props.onSelectDate(year, month, day);
  },

  handleSelectPrevMonth() {
    let { year, month } = this.state;

    if (--month === 0) {
      month = 12;
      year--;
    }

    this.setState({ year, month, day: null });
  },

  handleSelectNextMonth() {
    let { year, month } = this.state;

    if (++month > 12) {
      month = 1;
      year++;
    }

    this.setState({ year, month, day: null });
  },

  genMonthTable() {
    const data = this.getWeeklyMonthData();
    const rows = data.length;
    const cols = 7;

    const tableCaption = [0, 1, 2, 3, 4, 5, 6].map((i) => <td key={i}>{weekdayNumToName(i)}</td>);
    const tableContent = data.map((week) => {
      const days = week.map((day) => {
        let className = '';
        if (day.getDate() === this.state.day &&
            day.getMonth() === this.state.month - 1) className += 'selected ';
        if (day.getMonth() !== this.state.month - 1) className += 'inactive ';

        const isInTheFuture = isDateInTheFuture(day.getTime());
        let selectHandler = null;

        if (isInTheFuture) {
          className += 'inactive ';
        } else {
          selectHandler = this.handleSelectDate.bind(
            this,
            day.getFullYear(),
            day.getMonth() + 1,
            day.getDate()
          );
        }

        return (
          <td key={day.getTime()} className={className} onClick={selectHandler}>
            <span>{day.getDate()}</span>
          </td>
        );
      });

      return (
        <tr key={week[0].getTime()}>
          {days}
        </tr>
      );
    });

    return (
      <table rows={rows} cols={cols}>
        <thead><tr>{tableCaption}</tr></thead>
        <tbody>{tableContent}</tbody>
      </table>
    );
  },

  render() {
    const { year, month } = this.state;

    return (
      <div className="date-picker">
        <div className="header">
          <div className="arrow-left" onClick={this.handleSelectPrevMonth}>&lt;</div>
          <div className="year">{year}</div>
          <div className="month">{monthNumToName(parseInt(month, 10))}</div>
          <div className="arrow-right" onClick={this.handleSelectNextMonth}>&gt;</div>
        </div>
        <div className="body">
          {this.genMonthTable()}
        </div>
      </div>
    );
  },
});


export default DatePicker;
