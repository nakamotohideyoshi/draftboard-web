import React from 'react';


/**
 * Renders a list of a user's contest pool entries.
 */
const EntryList = React.createClass({

  propTypes: {
    entryCount: React.PropTypes.number.isRequired,
    contestPool: React.PropTypes.object.isRequired,
    removeContestPoolEntry: React.PropTypes.func.isRequired,
  },


  getEntryList(entryCount) {
    const entryList = [];

    for (let i = 0; i < entryCount; i++) {
      entryList.push(
        <tr key={`entry-${i}`}>
          <td className="contest-entry">
            <div className="contest-name">CONTEST NAME</div>
            <div
              className="button button--outline button--sm"
              onClick={this.props.removeContestPoolEntry}
            >
              Remove Entry
            </div>
          </td>
        </tr>
      );
    }

    return entryList;
  },


  render() {
    if (!this.props.entryCount) {
      return (
        <div>The selected lineup has no entries in this contest.</div>
      );
    }

    return (
      <div className="cmp-entry-list">
        <table className="table">
          <thead>
            <tr>
              <th className="title">Multi-Entries</th>
            </tr>
          </thead>
          <tbody>
            {this.getEntryList(this.props.entryCount)}
          </tbody>
        </table>
      </div>
    );
  },

});


module.exports = EntryList;
