import React from 'react';


/**
 * Renders a list of a user's contest pool entries.
 */
const EntryList = React.createClass({

  propTypes: {
    entries: React.PropTypes.array.isRequired,
    contestPoolInfo: React.PropTypes.object.isRequired,
    removeContestPoolEntry: React.PropTypes.func.isRequired,
  },


  getEntryList() {
    const entryList = this.props.entries.map((entry) =>
      <tr key={`entry-${entry.id}`}>
        <td className="contest-entry">
          <div className="contest-name">{this.props.contestPoolInfo.title}CONTEST NAME</div>
        </td>
        <td>
          <div
            className="button button--outline button--sm"
            onClick={this.handleRemoveClick.bind(null, entry.id)}
          >
            Remove Entry
          </div>
        </td>
      </tr>
    );

    return entryList;
  },


  handleRemoveClick(entryId) {
    this.props.removeContestPoolEntry(entryId);
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
