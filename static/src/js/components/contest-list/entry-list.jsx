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
  },


  getEntryList() {
    const entryList = this.props.entries.map((entry) => (
        <tr key={`entry-${entry.id}`}>
          <td className="contest-entry">
            <div className="lineup-name">{entry.lineup_name || 'Untitled Lineup'}</div>
          </td>
          <td>
            <UnregisterEntryButton
              entry={entry}
              onClick={this.props.removeContestPoolEntry}
            />
          </td>
        </tr>
      )
    );

    return entryList;
  },


  render() {
    if (!Object.keys(this.props.entries).length) {
      return (
        <div>The selected lineup has no entries in this contest.</div>
      );
    }

    return (
      <div className="cmp-entry-list">
        <table className="table">
          <thead>
            <tr>
              <th
                className="title"
                colSpan="2"
              >Multi-Entries</th>
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
