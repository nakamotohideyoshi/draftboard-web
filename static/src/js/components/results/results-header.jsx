import { dateNow } from '../../lib/utils';
import moment from 'moment';
import React from 'react';
import ResultsDaysSlider from './results-days-slider.jsx';
import ResultsDatePicker from './results-date-picker.jsx';


const ResultsHeader = React.createClass({

  propTypes: {
    year: React.PropTypes.number.isRequired,
    month: React.PropTypes.number.isRequired,
    day: React.PropTypes.number.isRequired,
    isWatchingLive: React.PropTypes.bool.isRequired,
    watchLiveLineups: React.PropTypes.func,
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

  returnToYesterday() {
    let theDate = new Date(dateNow());

    let delta = 1;  // days

    // We change results, draft groups, everything over at 10AM UTC, so
    // until then show the yesterdays results.
    if (theDate.getUTCHours() < 10) {
      delta = 2;
    }
    theDate.setDate(theDate.getDate() - delta);

    theDate = moment(theDate);

    this.props.onSelectDate(
      parseInt(theDate.format('YYYY'), 10),
      parseInt(theDate.format('M'), 10),
      parseInt(theDate.format('D'), 10)
    );
  },

  render() {
    const { year, month, day, isWatchingLive, onSelectDate, watchLiveLineups } = this.props;

    let lineupType = 'Live Lineups';
    let datePicker;
    let daySlider;

    let ctaLive = (
      <div className="watch-live-lineups" onClick={this.returnToYesterday}>
        See Past Lineups
      </div>
    );

    if (isWatchingLive === false) {
      lineupType = 'Past Lineups';

      daySlider = (
        <ResultsDaysSlider
          year={year}
          month={month}
          day={day}
          onSelectDate={onSelectDate}
        />
      );

      datePicker = (
        <ResultsDatePicker
          year={year}
          month={month}
          day={day}
          onSelectDate={onSelectDate}
        />
      );

      ctaLive = (
        <div className="watch-live-lineups" onClick={watchLiveLineups}>
          Watch Live Lineups
        </div>
      );
    }

    return (
      <div className="results-page--header">
        <div className="title">
          <div className="text">{lineupType}</div>
          <div className="date">{this.getTitle()}</div>
        </div>

        {daySlider}
        {datePicker}

        <div className="search">
          <div className="icon"></div>
        </div>
        <div className="cta">
          {ctaLive}
          <a href="/contests/" className="draft-a-team">
            Draft a team
          </a>
        </div>
      </div>
    );
  },

});


module.exports = ResultsHeader;
