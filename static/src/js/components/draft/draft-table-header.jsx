import React from 'react';
import log from '../../lib/logging.js';


const DraftTableHeader = React.createClass({

  propTypes: {
    text: React.PropTypes.string.isRequired,
    sortParam: React.PropTypes.string,
    onClick: React.PropTypes.func,
    additionalClasses: React.PropTypes.string,
  },

  handleClick() {
    if (this.props.onClick && this.props.sortParam) {
      this.props.onClick(this.props.sortParam);
    } else {
      log.warn('DraftTableHeader missing onClick or sortParam props.');
    }
  },

  render() {
    let classNames = this.props.sortParam ? 'table__sortable' : '';
    classNames += this.props.additionalClasses;
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
