import createBrowserHistory from 'history/lib/createBrowserHistory';
import moment from 'moment';
import React from 'react';
import renderComponent from '../../lib/render-component';
import ResultsHeader from './results-header.jsx';
import ResultsLineups from './results-lineups.jsx';
import ResultsStats from './results-stats.jsx';
import store from '../../store';
import { fetchResultsIfNeeded } from '../../actions/results';
import { Provider, connect } from 'react-redux';
import { Router, Route } from 'react-router';
import { syncReduxAndRouter } from 'redux-simple-router';
import { updatePath } from 'redux-simple-router';


const Results = React.createClass({

  propTypes: {
    dispatch: React.PropTypes.func.isRequired,
    params: React.PropTypes.object,
    results: React.PropTypes.object.isRequired,
  },

  getInitialState() {
    const yesterday = moment().subtract(1, 'day');

    return {
      year: yesterday.format('YYYY'),
      month: yesterday.format('MM'),
      day: yesterday.format('DD'),
      formattedDate: yesterday.format('YYYY-MM-DD'),
    };
  },

  componentWillMount() {
    const urlParams = this.props.params;
    let formattedDate = this.state.formattedDate;

    if (urlParams.hasOwnProperty('year')) {
      const newState = {
        year: parseInt(urlParams.year, 10),
        month: parseInt(urlParams.month, 10),
        day: parseInt(urlParams.day, 10),
      };
      newState.formattedDate = `${newState.year}-${newState.month}-${newState.day}`;

      this.setState(newState);
      formattedDate = newState.formattedDate;
    }

    this.props.dispatch(fetchResultsIfNeeded(formattedDate));
  },

  handleSelectDate(year, month, day) {
    const newState = {
      year,
      month,
      day,
      formattedDate: `${year}-${month}-${day}`,
    };

    this.setState(newState);
    this.props.dispatch(fetchResultsIfNeeded(newState.formattedDate));
    this.props.dispatch(updatePath(`/results/${newState.year}/${newState.month}/${newState.day}/`));
  },

  render() {
    const { year, month, day } = this.state;
    const dayResults = this.props.results[this.state.formattedDate] || null;

    let statsAndLineups;
    if (dayResults !== null) {
      statsAndLineups = (
        <div>
          <ResultsStats stats={dayResults.overall} />
          <ResultsLineups lineups={dayResults.lineups} />
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

// Which part of the Redux global state does our component want to receive as props?
const mapStateToProps = (state) => ({
  results: state.results,
});

// Wrap the component to inject dispatch and selected state into it.
const ResultsConnected = connect(
  mapStateToProps
)(Results);

// Set up to make sure that push states are synced with redux substore
const history = createBrowserHistory();
syncReduxAndRouter(history, store);

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
