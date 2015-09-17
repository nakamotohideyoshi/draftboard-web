'use strict';

var React = require('react');


/**
 * Render a single Player 'row'.
 *
 * @param {Object} row - A single row of the DataTable's data.
 * @param {array} columns - The columns that should be displayed. This is directly passed down
 * through DataTable.
 */
var ContestListRow = React.createClass({

  propTypes: {
    row: React.PropTypes.object.isRequired,
    focusedContestId: React.PropTypes.any,
    handleOnClick: React.PropTypes.func,
    draftable: React.PropTypes.bool
  },

  getInitialState: function() {
    return {};
  },


  getDefaultProps: function() {
    return {
      focusedContestId: '',
      draftable: true
    };
  },


  onClick: function(args) {
    console.log('onClick()', args);
    this.props.handleOnClick(args);
  },


  render: function() {
    // If it's the currently focused contest, add a class to it.
    var classes = this.props.focusedContestId === this.props.row.player_id ? 'active ' : '';
    classes += 'cmp-contest-list__row';

    if (this.props.draftable === false) {
      classes += ' fade';
    }

    return (
      <tr
        key={this.props.row.player_id}
        className={classes}
      >
        <td>{this.props.row.position}</td>
        <td>{this.props.row.first_name}{this.props.row.last_name} / {this.props.row.team_alias}</td>
        <td>STATUS</td>
        <td>OPP</td>
        <td>FPPG</td>
        <td>${this.props.row.salary.toLocaleString('en')}</td>
        <td>
          <div
            className="button--small--outline"
            onClick={this.onClick.bind(this, this.props.row.player_id)}
            >Draft</div>
        </td>
      </tr>
    );
  }

});


module.exports = ContestListRow;
