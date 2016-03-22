import * as ReactRedux from 'react-redux';
import React from 'react';
import LiveNBACourt from './live-nba-court';


/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
const mapStateToProps = (state) => ({
  animationEvents: state.pusherLive.animationEvents,
});

/**
 * Return the header section of the live page, including the lineup/contest title and overall stats
 */
const LiveAnimationArea = React.createClass({

  propTypes: {
    animationEvents: React.PropTypes.object.isRequired,
    liveSelector: React.PropTypes.object.isRequired,
    sport: React.PropTypes.string.isRequired,
  },

  /**
   * Typical react render method. What's interesting here is that we default to when there's just a lineup, then
   * modify the DOM elements if we're viewing a contest and/or an opponent.
   */
  render() {
    switch (this.props.sport) {
      case 'nba':
        return (
          <LiveNBACourt
            animationEvents={this.props.animationEvents}
            liveSelector={this.props.liveSelector}
          />
        );
      default:
        return (<div />);
    }
  },
});

// Set up Redux connections to React
const { connect } = ReactRedux;

// Wrap the component to inject dispatch and selected state into it.
const LiveAnimationAreaConnected = connect(
  mapStateToProps
)(LiveAnimationArea);

export default LiveAnimationAreaConnected;
