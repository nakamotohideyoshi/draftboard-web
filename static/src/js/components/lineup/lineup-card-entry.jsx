import React from 'react';


const LineupCardEntry = React.createClass({

  propTypes: {
    entry: React.PropTypes.object.isRequired,
    removeEntry: React.PropTypes.object.isRequired,
  },


  handleRemoveEntry() {
    this.props.removeEntry();
  },


  render() {
    return (
      <li className="entry">
        <span className="remove"><span className="button-remove">x</span></span>
        <span className="contest">{this.props.entry.contest.name}</span>
        <span className="fees">
          ${this.props.entry.contest.buyin.toLocaleString('en')} x {this.props.entry.entryCount}
        </span>
      </li>
    );
  },
});


module.exports = LineupCardEntry;
