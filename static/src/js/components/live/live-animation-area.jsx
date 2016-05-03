import * as ReactRedux from 'react-redux';
import React from 'react';
import LiveMLBStadium from './mlb/live-mlb-stadium';
import LiveNBACourt from './live-nba-court';


/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
const mapStateToProps = (state) => ({
  animationEvents: state.events.animationEvents,
});

/**
 * Return the header section of the live page, including the lineup/contest title and overall stats
 */
const LiveAnimationArea = (props) => {
  switch (props.sport) {
    case 'mlb':
      return (
        <LiveMLBStadium
          animationEvents={props.animationEvents}
          multipartEvents={props.multipartEvents}
        />
      );
    case 'nba':
      return (
        <LiveNBACourt animationEvents={props.animationEvents} />
      );
    default:
      return (<div />);
  }
};

LiveAnimationArea.propTypes = {
  animationEvents: React.PropTypes.object.isRequired,
  multipartEvents: React.PropTypes.object.isRequired,
  sport: React.PropTypes.string.isRequired,
};

// Set up Redux connections to React
const { connect } = ReactRedux;

// Wrap the component to inject dispatch and selected state into it.
const LiveAnimationAreaConnected = connect(
  mapStateToProps
)(LiveAnimationArea);

export default LiveAnimationAreaConnected;
