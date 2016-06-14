import { connect } from 'react-redux';
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
  eventsMultipart: state.eventsMultipart,
  watching: state.watching,
});

/**
 * Return the header section of the live page, including the lineup/contest title and overall stats
 */
export const LiveAnimationArea = (props) => {
  switch (props.watching.sport) {
    case 'mlb':
      return (
        <LiveMLBStadium
          animationEvents={props.animationEvents}
          eventsMultipart={props.eventsMultipart}
          watching={props.watching}
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
  eventsMultipart: React.PropTypes.object.isRequired,
  watching: React.PropTypes.object.isRequired,
};

// Wrap the component to inject dispatch and selected state into it.
export default connect(
  mapStateToProps
)(LiveAnimationArea);
