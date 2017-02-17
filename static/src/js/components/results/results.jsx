import map from 'lodash/map';
import moment from 'moment';
import React from 'react';
import renderComponent from '../../lib/render-component';
import ResultsStatic from './results-static.jsx';
import store from '../../store';
import uniqBy from 'lodash/uniqBy';
import { dateNow } from '../../lib/utils';
import { fetchCurrentLineupsAndRelated } from '../../actions/current-lineups';
import { fetchResultsIfNeeded, fetchEntryResults } from '../../actions/results';
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
export const Results = React.createClass({

  propTypes: {
    dispatch: React.PropTypes.func.isRequired,
    hasRelatedInfo: React.PropTypes.bool.isRequired,
    params: React.PropTypes.object,
    route: React.PropTypes.object,
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
      isWatchingLive: null,
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
    } else if (this.props.route.path === '/results/live-with-lineups/') {
      this.watchLiveLineups();
    } else {
      let theDate = new Date(dateNow());
      let delta = 1;  // days

      // We change results, draft groups, everything over at 10AM UTC, so
      // until then show the yesterdays results.
      if (theDate.getUTCHours() < 10) {
        delta = 2;
      }
      theDate.setDate(theDate.getDate() - delta);

      // for easier formatting
      theDate = moment(theDate);

      this.handleSelectDate(
        parseInt(theDate.format('YYYY'), 10),
        parseInt(theDate.format('M'), 10),
        parseInt(theDate.format('D'), 10)
      );
    }
  },

  componentDidUpdate(prevProps) {
    if (
      prevProps.hasRelatedInfo === false &&
      this.props.hasRelatedInfo === true &&
      this.state.isWatchingLive === true
    ) {
      this.props.dispatch(updateLiveMode({
        sport: map(
          uniqBy(this.props.resultsWithLive.lineups, 'sport'),
          lineup => lineup.sport
        ),
      }));
    }
  },

  handleSelectDate(year, month, day) {
    const newState = {
      year,
      month,
      day,
      formattedDate: `${year}-${month}-${day}`,
      isWatchingLive: false,
    };

    this.setState(newState);
    this.props.dispatch(fetchResultsIfNeeded(newState.formattedDate));

    this.props.dispatch(routerPush(`/results/${year}/${month}/${day}/`));
  },

  watchLiveLineups() {
    this.props.dispatch(fetchCurrentLineupsAndRelated(true));

    let theDate = new Date(dateNow());

    // We change results, draft groups, everything over at 10AM UTC, so
    // until then show the yesterdays results.
    if (theDate.getUTCHours() < 10) {
      theDate.setDate(theDate.getDate() - 1);
    }

    theDate = moment(theDate);

    const newState = {
      year: parseInt(theDate.format('YYYY'), 10),
      month: parseInt(theDate.format('M'), 10),
      day: parseInt(theDate.format('D'), 10),
      isWatchingLive: true,
    };
    newState.formattedDate = `${newState.year}-${newState.month}-${newState.day}`;

    this.setState(newState);

    this.props.dispatch(routerPush('/results/live-with-lineups/'));
  },

  render() {
    return (
        <ResultsStatic
          params={this.props.params}
          results={this.props.results}
          resultsWithLive={this.props.resultsWithLive}
          onSelectDate={this.handleSelectDate}
          date={this.state}
          watchLiveLineups={this.watchLiveLineups}
          fetchEntryResults={(entryId) => this.props.dispatch(fetchEntryResults(entryId))}
        />
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
      <Route path="/results/live-with-lineups/" component={ResultsConnected} />
      <Route path="/results/:year/:month/:day/" component={ResultsConnected} />
    </Router>
  </Provider>,
  '.results-page'
);
