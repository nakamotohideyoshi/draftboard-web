import React from 'react';
import { Provider, connect } from 'react-redux';

import store from '../../store';
import { fetchLineups } from '../../actions/results';
import renderComponent from '../../lib/render-component';

import ResultsStats from './results-stats.jsx';
import ResultsHeader from './results-header.jsx';
import ResultsLineups from './results-lineups.jsx';
import ResultsDaysSlider from './results-days-slider.jsx';
import ResultsDatePicker from './results-date-picker.jsx';

const Results = React.createClass({

  propTypes: {
    stats: React.PropTypes.object.isRequired,
    lineups: React.PropTypes.array.isRequired,
    dispatch: React.PropTypes.func.isRequired,
  },

  getInitialState() {
    const today = new Date();

    return {
      year: today.getFullYear(),
      month: today.getMonth(),
      day: today.getDate(),
    };
  },

  componentWillMount() {
    const { year, month, day } = this.state;
    // TODO: Add real data.
    this.props.dispatch(fetchLineups(10, new Date(year, month, day)));
  },

  handleSelectDate(year, month, day) {
    this.setState({ year, month, day });
  },

  render() {
    return (
      <div className="inner">
        <ResultsHeader>
          <ResultsDaysSlider year={this.state.year}
            month={this.state.month}
            day={this.state.day}
            onSelectDate={this.handleSelectDate}
          />
          <ResultsDatePicker year={this.state.year}
            month={this.state.month}
            day={this.state.day}
            onSelectDate={this.handleSelectDate}
          />
        </ResultsHeader>
        <ResultsStats stats={this.props.stats} />
        <ResultsLineups lineups={this.props.lineups} />
      </div>
    );
  },
});

// Which part of the Redux global state does our component want to receive as props?
const mapStateToProps = (state) => ({
  stats: state.results.stats,
  lineups: state.results.lineups,
});

// Wrap the component to inject dispatch and selected state into it.
const ResultsConnected = connect(
  mapStateToProps
)(Results);

renderComponent(
  <Provider store={store}>
    <ResultsConnected />
  </Provider>,
  '.results-page'
);

export default ResultsConnected;
