import moment from 'moment';
import React from 'react';
import ResultsDaysSlider from './results-days-slider.jsx';
import ResultsDatePicker from './results-date-picker.jsx';


const ResultsHeader = React.createClass({

  propTypes: {
    year: React.PropTypes.number.isRequired,
    month: React.PropTypes.number.isRequired,
    day: React.PropTypes.number.isRequired,
    onSelectDate: React.PropTypes.func,
  },

  getTitle() {
    const { year, month, day } = this.props;
    return moment(`${year}-${month}-${day}`, 'YYYY-M-D').calendar(null, {
      sameDay: '[Today], MMMM D, YYYY',
      nextDay: '[Tomorrow], MMMM D, YYYY',
      nextWeek: 'dddd, MMMM D, YYYY',
      lastDay: '[Yesterday], MMMM D, YYYY',
      lastWeek: '[Last] dddd, MMMM D, YYYY',
      sameElse: 'MMMM D, YYYY',
    });
  },

  render() {
    const { year, month, day, onSelectDate } = this.props;

    return (
      <div className="results-page--header">
        <div className="title">
          <div className="text">Active & upcoming lineups</div>
          <div className="date">{this.getTitle()}</div>
        </div>

        <ResultsDaysSlider
          year={year}
          month={month}
          day={day}
          onSelectDate={onSelectDate}
        />
        <ResultsDatePicker
          year={year}
          month={month}
          day={day}
          onSelectDate={onSelectDate}
        />

        <div className="search">
          <div className="icon"></div>
        </div>
        <a href="/lobby/" className="draft-a-team">
          Draft a team
        </a>
      </div>
    );
  },

});


module.exports = ResultsHeader;
