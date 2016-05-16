import React from 'react';
import UnregisterEntryButton from './unregister-entry-button.jsx';
import find from 'lodash/find';

/**
 * Renders a list of a user's contest pool entries for use in the contest
 * detail pane.
 */
const EntryList = React.createClass({

  propTypes: {
    entries: React.PropTypes.array.isRequired,
    contestPoolInfo: React.PropTypes.object.isRequired,
    removeContestPoolEntry: React.PropTypes.func.isRequired,
    unregisterRequests: React.PropTypes.object.isRequired,
  },


  getEntryList() {
    const entryList = this.props.entries.map((entry) => {
      const unregisterRequest = find(this.props.unregisterRequests,
        (request) => request.entryId === entry.id
      );

      return (
        <tr key={`entry-${entry.id}`}>
          <td className="contest-entry">
            <div className="contest-name">{this.props.contestPoolInfo.contest.name}</div>
          </td>
          <td>
            <UnregisterEntryButton
              entry={entry}
              unregisterRequest={unregisterRequest}
              onClick={this.props.removeContestPoolEntry}
            />
          </td>
        </tr>
      );
    });

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
