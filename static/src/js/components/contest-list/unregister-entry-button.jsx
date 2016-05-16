import React from 'react';

/**
 * Button that will remove a lineup entry from a contest.
 */
const UnregisterEntryButton = React.createClass({

  propTypes: {
    unregisterRequest: React.PropTypes.object.isRequired,
    entry: React.PropTypes.object.isRequired,
    onClick: React.PropTypes.func.isRequired,
  },

  handleOnClick(entry) {
    this.props.onClick(entry);
  },


  renderWorkingButton() {
    return (
      <div
        className="pull-right button button--outline button--sm button--working"
      >
        Removing...
      </div>
    );
  },


  render() {
    if (this.props.unregisterRequest) {
      return (
        this.renderWorkingButton(this.props.unregisterRequest)
      );
    }

    return (
      <div
        className="pull-right button button--outline button--sm"
        onClick={this.handleOnClick.bind(null, this.props.entry)}
      >
        Remove Entry
      </div>
    );
  },
});


module.exports = UnregisterEntryButton;
