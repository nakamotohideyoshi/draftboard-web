import React from 'react';
import log from '../../lib/logging.js';


const DraftTableHeader = React.createClass({

  propTypes: {
    text: React.PropTypes.string.isRequired,
    sortParam: React.PropTypes.string,
    onClick: React.PropTypes.func,
  },

  handleClick() {
    if (this.props.onClick && this.props.sortParam) {
      this.props.onClick(this.props.sortParam);
    } else {
      log.warn('DraftTableHeader missing onClick or sortParam props.');
    }
  },

  render() {
    const classNames = this.props.sortParam ? 'table__sortable' : '';

    return (
      <th
        className={classNames}
        onClick={this.handleClick}
      >
        {this.props.text}
      </th>
    );
  },
});


module.exports = DraftTableHeader;
