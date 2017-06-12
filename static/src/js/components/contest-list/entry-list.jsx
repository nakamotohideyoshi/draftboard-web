import React from 'react';
import UnregisterEntryButton from './unregister-entry-button.jsx';


/**
 * Renders a list of a user's contest pool entries for use in the contest
 * detail pane.
 */
const EntryList = React.createClass({

  propTypes: {
    entries: React.PropTypes.array.isRequired,
    contestPoolInfo: React.PropTypes.object.isRequired,
    removeContestPoolEntry: React.PropTypes.func.isRequired,
    user: React.PropTypes.object,
  },


  getEntryList() {
    const entryList = this.props.entries.map((entry) => {
      let icon = '';
      if (entry === this.props.entries[0]) {
        icon = (
          <span
            className="icon-guaranteed"
            title="Your first entry is guaranteed to be placed in a contest. Subsequent
            entries are not guaranteed. Any entries not placed in contests will be refunded."
          ></span>);
      }

      return (
        <tr key={`entry-${entry.id}`}>
          <td className="contest-entry">
            <div className="lineup-name">{this.props.user.username || 'Your Lineup'} {icon} </div>
          </td>
          <td>
            <UnregisterEntryButton
              entry={entry}
              onClick={this.props.removeContestPoolEntry}
            />
          </td>
        </tr>
      );
    });

    return entryList;
  },


  render() {
    return (
      <div className="cmp-entry-list">
        <table className="table">
          <thead>
            <tr>
              <th
                className="title"
                colSpan="2"
              >Entries</th>
            </tr>
          </thead>
          <tbody>
            {this.getEntryList()}
          </tbody>
        </table>
      </div>
    );
  },

});


module.exports = EntryList;
