const React = require('react')
const moment = require('moment')
import CountdownClock from '../site/countdown-clock.jsx'


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
    focusedLineup: React.PropTypes.object,
    focusedContest: React.PropTypes.object,
    highlighted: React.PropTypes.bool,
    enterContest: React.PropTypes.func,
    setFocusedContest: React.PropTypes.func,
    draftGroupsWithLineups: React.PropTypes.array,
    isEntered: React.PropTypes.bool
  },


  handleRowClick: function(contest) {
    this.props.setFocusedContest(contest);
  },


  ignoreClick: function(e) {
    e.stopPropagation();
  },


  getEnterButton: function() {
    if (this.props.isEntered) {
      return (
        <span
          className="button button--mini button--green disabled"
          onClick={this.ignoreClick}
        >
          Entered
        </span>
      )
    }
    // Is the currently focused lineup able to enter this contest?
    if (this.props.focusedLineup && this.props.focusedLineup.draft_group === this.props.row.draft_group) {
      return (
        <span
          className="button button--mini--outline button--green-outline"
          onClick={this.props.enterContest.bind(null, this.props.row)}>
          Enter
        </span>
      )
    } else {
      return (
        <a
          className="button button--mini--outline button--green-outline"
          title="Draft a lineup for this contest."
          href={'/draft/' + this.props.row.draft_group + '/'}
          onClick={this.ignoreClick}
        >
          Draft
        </a>
      )
    }
  },


  render: function() {
    // If it's the currently focused contest, add a class to it.
    var classes = this.props.focusedContest.id === this.props.row.id ? 'active ' : '';
    classes += 'cmp-contest-list__row';
    if (this.props.isEntered) {
      classes += ' entered'
    }

    if (this.props.highlighted) {
      classes += ' highlight'
    }

    // Icons
    var guaranteedIcon;
    if (this.props.row.gpp) {
      guaranteedIcon = <span className="contest-icon contest-icon__guaranteed">G</span>;
    }
    var multiEntryIcon;
    if (this.props.row.max_entries > 1) {
      multiEntryIcon = <span className="contest-icon contest-icon__multi-entry">M</span>;
    }

    let enterButton = this.getEnterButton()

    return (
      <tr
        onClick={this.handleRowClick.bind(this, this.props.row)}
        key={this.props.row.id}
        className={classes}
      >
        <td key="sport" className="sport">
          <span className={"icon icon-" + this.props.row.sport}></span>
        </td>
        <td key="name" className="name">{this.props.row.name} {guaranteedIcon}</td>
        <td key="entries" className="entries">{multiEntryIcon} {this.props.row.current_entries}/{this.props.row.entries}</td>
        <td key="fee" className="fee">${this.props.row.buyin}</td>
        <td key="prizes" className="prizes">${this.props.row.prize_pool}</td>
        <td key="start" className="start"><CountdownClock time={this.props.row.start} /></td>

        <td className="enter">
          {enterButton}
        </td>
      </tr>
    );
  }

});


module.exports = ContestListRow;
