import map from 'lodash/map';
import moment from 'moment';
import React from 'react';
import renderComponent from '../../lib/render-component';
import ResultsHeader from './results-header.jsx';
import ResultsLineups from './results-lineups.jsx';
import ResultsStats from './results-stats.jsx';
import store from '../../store';
import uniqBy from 'lodash/uniqBy';
import { dateNow } from '../../lib/utils';
import { fetchCurrentLineupsAndRelated } from '../../actions/current-lineups';
import { fetchResultsIfNeeded } from '../../actions/results';
import { liveContestsSelector } from '../../selectors/live-contests';
import { myCurrentLineupsSelector } from '../../selectors/current-lineups';
import { Provider, connect } from 'react-redux';
import { push as routerPush } from 'react-router-redux';
import { resultsWithLive } from '../../selectors/results-with-live';
import { Router, Route, browserHistory } from 'react-router';
import { sportsSelector } from '../../selectors/sports';
import { syncHistoryWithStore } from 'react-router-redux';
import { updateLiveMode } from '../../actions/watching';
import { lineupsHaveRelatedInfoSelector } from '../../selectors/current-lineups';

/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
const mapStateToProps = (state) => ({
  hasRelatedInfo: lineupsHaveRelatedInfoSelector(state),
  myCurrentLineupsSelector: myCurrentLineupsSelector(state),
  liveContestsSelector: liveContestsSelector(state),
  results: state.results,
  resultsWithLive: resultsWithLive(state),
  sportsSelector: sportsSelector(state),
});

/*
 * The overarching component for the results section.
 */
const Results = React.createClass({

  propTypes: {
    dispatch: React.PropTypes.func.isRequired,
    hasRelatedInfo: React.PropTypes.bool.isRequired,
    params: React.PropTypes.object,
    results: React.PropTypes.object.isRequired,
    myCurrentLineupsSelector: React.PropTypes.object.isRequired,
    liveContestsSelector: React.PropTypes.object.isRequired,
    resultsWithLive: React.PropTypes.object.isRequired,
    sportsSelector: React.PropTypes.object.isRequired,
  },

  /**
   * Default initial state to today
   * @return {object} Initial state
   */
  getInitialState() {
    return {
      year: null,
      month: null,
      day: null,
      dateIsToday: null,
      formattedDate: null,
    };
  },

  /**
   * Once we have access to URL, check and update to date if it exists
   */
  componentWillMount() {
    const urlParams = this.props.params;

    if (urlParams.hasOwnProperty('year')) {
      this.handleSelectDate(
        parseInt(urlParams.year, 10),
        parseInt(urlParams.month, 10),
        parseInt(urlParams.day, 10)
      );
    } else {
      const today = moment(dateNow());

      this.handleSelectDate(
        parseInt(today.format('YYYY'), 10),
        parseInt(today.format('M'), 10),
        parseInt(today.format('D'), 10)
      );
    }
  },

  componentDidUpdate(prevProps) {
    if (prevProps.hasRelatedInfo === false && this.props.hasRelatedInfo === true) {
      if (this.state.dateIsToday === true) {
        this.props.dispatch(updateLiveMode({
          sport: map(
            uniqBy(this.props.resultsWithLive.lineups, 'sport'),
            lineup => lineup.sport
          ),
        }));
      }
    }
  },

  handleSelectDate(year, month, day) {
    const newState = {
      dateObject: new Date(year, month, day),
      year,
      month,
      day,
      formattedDate: `${year}-${month}-${day}`,
    };

    this.setState(newState);

    const today = moment(dateNow());
    const todayFormatted = today.format('YYYY-M-D');

    // if we are dealing with today, then get entries
    if (newState.formattedDate === todayFormatted) {
      this.setState({ dateIsToday: true });

      this.props.dispatch(fetchCurrentLineupsAndRelated(true));
    } else {
      this.setState({ dateIsToday: false });
      this.props.dispatch(fetchResultsIfNeeded(newState.formattedDate));
    }

    this.props.dispatch(routerPush(`/results/${newState.year}/${newState.month}/${newState.day}/`));
  },

  render() {
    const { year, month, day } = this.state;

    let dayResults = this.props.results[this.state.formattedDate] || null;
    if (this.state.dateIsToday === true) {
      dayResults = this.props.resultsWithLive || null;
    }

    let statsAndLineups;
    if (dayResults !== null) {
      statsAndLineups = (
        <div>
          <ResultsStats stats={dayResults.overall} />
          <ResultsLineups
            dateIsToday={this.state.dateIsToday}
            lineups={dayResults.lineups}
          />
        </div>
      );
    }

    return (
      <div className="inner">
        <ResultsHeader
          year={year}
          month={month}
          day={day}
          onSelectDate={this.handleSelectDate}
        />
        {statsAndLineups}
      </div>
    );
  },
});

// Wrap the component to inject dispatch and selected state into it.
const ResultsConnected = connect(
  mapStateToProps
)(Results);

// Create an enhanced history that syncs navigation events with the store
const history = syncHistoryWithStore(browserHistory, store);

// Uses the Provider and Routes in order to have URL routing via redux-simple-router and redux state
renderComponent(
  <Provider store={store}>
    <Router history={history}>
      <Route path="/results/" component={ResultsConnected} />
      <Route path="/results/:year/:month/:day/" component={ResultsConnected} />
    </Router>
  </Provider>,
  '.results-page'
);
