import moment from 'moment';
import React from 'react';
import ResultsHeader from './results-header.jsx';
import ResultsLineups from './results-lineups.jsx';
import ResultsStats from './results-stats.jsx';
import { dateNow } from '../../lib/utils';

/*
 * The overarching component for the results section.
 */
const ResultsStatic = React.createClass({
  propTypes: {
    params: React.PropTypes.object,
    results: React.PropTypes.object.isRequired,
    date: React.PropTypes.shape({
      year: React.PropTypes.number,
      month: React.PropTypes.number,
      day: React.PropTypes.number,
      dateIsToday: React.PropTypes.boolean,
      formattedDate: React.PropTypes.string,
    }),
    onSelectDate: React.PropTypes.func.isRequired,
    resultsWithLive: React.PropTypes.object.isRequired,
  },

  /**
   * Once we have access to URL, check and update to date if it exists
   */
  componentWillMount() {
    const urlParams = this.props.params;

    if (urlParams.hasOwnProperty('year')) {
      this.props.onSelectDate(
        parseInt(urlParams.year, 10),
        parseInt(urlParams.month, 10),
        parseInt(urlParams.day, 10)
      );
    } else {
      const today = moment(dateNow());

      // We change results, draft groups, everything over at 10AM UTC, so
      // until then show the yesterdays results.
      if (today.hour() < 10) {
        today.add(-1, 'days');
      }

      this.props.onSelectDate(
        parseInt(today.format('YYYY'), 10),
        parseInt(today.format('M'), 10),
        parseInt(today.format('D'), 10)
      );
    }
  },

  render() {
    const { year, month, day, dateIsToday, formattedDate } = this.props.date;

    let dayResults = this.props.results[formattedDate] || null;
    if (dateIsToday === true) {
      dayResults = this.props.resultsWithLive || null;
    }

    let statsAndLineups;
    if (dayResults !== null) {
      statsAndLineups = (
        <div>
          <ResultsStats stats={dayResults.overall} />
          <ResultsLineups
            dateIsToday={dateIsToday}
            lineups={dayResults.lineups}
          />
        </div>
      );
    } else {
      // Show empty stats line to prevent rendering glitches.
      statsAndLineups = (
        <div>
          <ResultsStats />
        </div>
      );
    }

    return (
      <div className="inner">
        <ResultsHeader
          year={year}
          month={month}
          day={day}
          onSelectDate={this.props.onSelectDate}
        />
        {statsAndLineups}
      </div>
    );
  },
});

export default ResultsStatic;
