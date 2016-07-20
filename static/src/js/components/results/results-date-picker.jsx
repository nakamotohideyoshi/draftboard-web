import React from 'react';
import ReactDOM from 'react-dom';
import PureRenderMixin from 'react-addons-pure-render-mixin';

import DatePicker from '../site/date-picker.jsx';

const ResultsDatePicker = React.createClass({

  propTypes: {
    year: React.PropTypes.number.isRequired,
    month: React.PropTypes.number.isRequired,
    day: React.PropTypes.number.isRequired,
    onSelectDate: React.PropTypes.func.isRequired,
  },

  mixins: [PureRenderMixin],

  getInitialState() {
    return { shown: false };
  },

  componentWillMount() {
    document.body.addEventListener('click', this.handleHide, false);
  },

  componentWillUnmount() {
    document.body.removeEventListener('click', this.handleHide);
  },

  handleToggle() {
    this.setState({ shown: !this.state.shown });
  },

  handleHide(e) {
    if (ReactDOM.findDOMNode(this).contains(e.target)) return;

    this.setState({ shown: false });
  },

  handleSelectDate(year, month, day) {
    this.props.onSelectDate(year, month + 1, day);
  },

  render() {
    const datePicker = this.state.shown ? (
      <DatePicker year={this.props.year}
        month={this.props.month - 1}
        day={this.props.day}
        onSelectDate={this.handleSelectDate}
      />
    ) : null;

    return (
      <div className="results-date-picker">
        <div className="toggle" onClick={this.handleToggle}></div>
        {datePicker}
      </div>
    );
  },

});


export default ResultsDatePicker;
