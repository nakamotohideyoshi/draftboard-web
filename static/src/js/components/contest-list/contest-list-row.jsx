const React = require('react')
const moment = require('moment')
import * as AppActions from '../../stores/app-state-store.js'
import {timeRemaining} from '../../lib/utils.js'


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
    focusedContestId: React.PropTypes.any,
    enterContest: React.PropTypes.func,
    setFocusedContest: React.PropTypes.func
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


  handleRowClick: function(contest) {
    AppActions.openPane();
    this.props.setFocusedContest(contest);
  },


  componentDidMount: function() {
    this.setTimeRemaining();
    this.updateTimeRemainingLoop = window.setInterval(this.setTimeRemaining, 1000);
  },


  componentWillUnmount: function() {
    window.clearInterval(this.updateTimeRemainingLoop);
  },


  setTimeRemaining: function() {
    // difference between when the contest starts and now.
    this.setState({
      timeRemaining: timeRemaining(this.props.row.start)
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
        onClick={this.handleRowClick.bind(this, this.props.row)}
        key={this.props.row.id}
        className={classes}
      >
        <td key="sport" className="sport">
          <span className={"icon icon-" + this.props.row.sport}>{this.props.row.sport}</span>
        </td>
        <td key="name" className="name">{this.props.row.name}</td>
        <td key="entries" className="entries">{multiEntryIcon} {this.props.row.current_entries}/{this.props.row.entries}</td>
        <td key="fee" className="fee">{this.props.row.buyin}</td>
        <td key="prizes" className="prizes">{guaranteedIcon} {this.props.row.buyin}</td>
        <td key="start" className="start">{timeRemaining}</td>

        <td className="cmp-contest-list__cell">
          <span className="button--mini--outline button--green-outline" onClick={this.props.enterContest.bind(null, this.props.row.id)}>Enter</span>
        </td>
      </tr>
    );
  }

});


module.exports = ContestListRow;
