'use strict';

var React = require('react');
var ContestActions = require('../../actions/contest-actions');
var MultiEntryButton = require('./multi-entry-button.jsx');
var moment = require('moment');


/**
 * Render a single ContestList 'row'.
 * contest list specific functionality.
 *
 * Clicking the row sets it as the active contest in the Store.
 *
 * @param {Object} row - A single row of the DataTable's data.
 * @param {array} columns - The columns that should be displayed. This is directly passed down
 * through DataTable.
 */
var ContestListRow = React.createClass({

  propTypes: {
    row: React.PropTypes.object.isRequired,
    columns: React.PropTypes.array,
    focusedContestId: React.PropTypes.any
  },

  getInitialState: function() {
    return {
      timeRemaining: {
        days: '',
        hours: '',
        minutes: '',
        seconds: ''
      }
    };
  },


  componentDidMount: function() {
    this.setTimeRemaining();
    this.updateTimeRemainingLoop = window.setInterval(this.setTimeRemaining, 1000);
  },


  componentWillUnmount: function() {
    window.clearInterval(this.updateTimeRemainingLoop);
  },


  getDefaultProps: function() {
    return {
      focusedContestId: ''
    };
  },


  /**
   * When a row is clicked (or something else) we want to make that contest the 'focused' one.
   * @param {integer} id the ID of the contest to be focused.
   * @param {Object} e  Click event - Supplied by the click handler.
   */
  setContestFocus: function(id) {
    if (typeof id === 'number') {
      ContestActions.contestFocused(id);
    }
  },


  addLeadingZero: function(number) {
    return (Math.abs(number) < 10) ? "0" + Math.abs(number) : Math.abs(number);
  },


  setTimeRemaining: function() {
    // difference between when the contest starts and now (in ms).
    var diffTime = moment.utc(this.props.row.start) - moment();
    // convert to a moment 'duration' so we can parse it out.
    var duration = moment.duration(diffTime);

    this.setState({
        timeRemaining: {
          hours: Math.floor(duration.asHours()),
          minutes: this.addLeadingZero(duration.minutes()),
          seconds: this.addLeadingZero(duration.seconds())
        }
    });
  },


  render: function() {
    // If it's the currently focused contest, add a class to it.
    var classes = this.props.focusedContestId === this.props.row.id ? 'active ' : '';
    classes += 'cmp-contest-list__row';

    // Icons
    var guaranteedIcon;
    if (this.props.row.gpp) {
      guaranteedIcon = <span className="contest-icon contest-icon__guaranteed">G</span>;
    }
    var multiEntryIcon;
    if (this.props.row.max_entries > 1) {
      multiEntryIcon = <span className="contest-icon contest-icon__multi-entry">M</span>;
    }

    var timeRemaining = (
      <span className="contest-list__live-in">
        <span className="contest-list__live-in-hours">{this.state.timeRemaining.hours}:</span>
        <span className="contest-list__live-in-minutes">{this.state.timeRemaining.minutes}:</span>
        <span className="contest-list__live-in-seconds">{this.state.timeRemaining.seconds}</span>
      </span>
    );

    return (
      <tr
        onClick={this.setContestFocus.bind(this, this.props.row.id)}
        key={this.props.row.id}
        className={classes}
      >
        <td key="sport" className="sport">
          <span className={"icon icon-" + this.props.row.sport}>{this.props.row.sport}</span>
        </td>
        <td key="name" className="name">{this.props.row.name}</td>
        <td key="entries" className="entries">{multiEntryIcon} {this.props.row.current_entries}/{this.props.row.entries}</td>
        <td key="fee" className="fee">{this.props.row.prize_structure.buyin}</td>
        <td key="prizes" className="prizes">{guaranteedIcon} {this.props.row.prize_structure.buyin}</td>
        <td key="start" className="start">{timeRemaining}</td>

        <td className="cmp-contest-list__cell">
          <MultiEntryButton />
        </td>
      </tr>
    );
  }

});


module.exports = ContestListRow;
