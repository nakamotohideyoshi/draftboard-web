import { connect } from 'react-redux';
import LiveOverallStats from './live-overall-stats';
import React from 'react';
import { generateBlockNameWithModifiers } from '../../lib/utils/bem';

// assets
require('../../../sass/blocks/live/live-header.scss');


/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
const mapStateToProps = (state) => ({
  animationEvent: state.events.animationEvent,
  showEventResult: state.events.showEventResult,
  eventsMultipart: state.eventsMultipart,
  watching: state.watching,
});

/**
 * Return the header section of the live page, including the lineup/contest title and overall stats
 */
export const LiveHeader = (props) => {
  const { myLineup, contest, opponentLineup, watching } = props;

  // show nothing if loading
  if (myLineup.isLoading !== false) return null;

  // animation description
  const modifiers = ['show'];
  const liveOverallStatsModifiers = [];
  let currentAnimationInfo = null;

  if (props.showEventResult === true) {
    const classNames = generateBlockNameWithModifiers('live-header__animation-info', modifiers);
    liveOverallStatsModifiers.push('event-ended');

    currentAnimationInfo = (
      <div className={classNames}>
        <h2 className="live-header__animation-info__type">
          {`${props.animationEvent.type.toUpperCase()}!`}
        </h2>
        <div className="live-header__animation-info__description">
          {props.animationEvent.description}
        </div>
      </div>
    );
  }

  // set all needed variables, and default them to lineup only
  let opponentStats;
  let statsVs;
  let { potentialWinnings, rank } = myLineup;

  // if watching a contest, then update the titles and ensure the overall stats are contest-based
  if (watching.contestId !== null && contest.isLoading === false) {
    potentialWinnings = contest.potentialWinnings;
    rank = contest.rank;

    // if watching an opponent, then add in second overall stats and update the titles
    if (watching.opponentLineupId !== null && opponentLineup.isLoading === false) {
      statsVs = (
        <div className="live-overall-stats__vs">vs</div>
      );
      opponentStats = (
        <LiveOverallStats
          fp={opponentLineup.fp}
          id={opponentLineup.id}
          modifiers={liveOverallStatsModifiers}
          name={opponentLineup.name}
          potentialWinnings={potentialWinnings}
          rank={rank}
          timeRemaining={opponentLineup.timeRemaining}
          whichSide="opponent"
        />
      );
    }
  }


  return (
    <header className="live-header">
      <LiveOverallStats
        fp={myLineup.fp}
        id={myLineup.id}
        name={myLineup.name}
        modifiers={liveOverallStatsModifiers}
        potentialWinnings={potentialWinnings}
        rank={rank}
        timeRemaining={myLineup.timeRemaining}
        whichSide="mine"
      />

      {statsVs}
      {opponentStats}
      {currentAnimationInfo}
    </header>
  );
};

LiveHeader.propTypes = {
  animationEvent: React.PropTypes.object,
  contest: React.PropTypes.object.isRequired,
  myLineup: React.PropTypes.object.isRequired,
  opponentLineup: React.PropTypes.object.isRequired,
  showEventResult: React.PropTypes.bool.isRequired,
  watching: React.PropTypes.object.isRequired,
};

// Wrap the component to inject dispatch and selected state into it.
export default connect(
  mapStateToProps
)(LiveHeader);
