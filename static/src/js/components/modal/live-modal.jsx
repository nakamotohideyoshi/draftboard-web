import React from 'react';
import Model from './model';

const LiveModal = React.createClass({
  propTypes: {
    sport: React.PropTypes.string.required,
  },
  onClose() {
    return false;
  },
  isOpen() {
    return true;
  },
  render() {
    return (
      <Model
        showCloseBtn="true"
        isOpen={this.isOpen}
        onClose={this.onClose}
        className="live-notice"
      >
        <h1>hello world</h1>
      </Model>
    );
  },
});

module.exports = LiveModal;
