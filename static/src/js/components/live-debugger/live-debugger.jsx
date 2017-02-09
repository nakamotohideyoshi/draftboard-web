import { connect } from 'react-redux';
import React from 'react';
import LiveAnimationArea from '../live/live-animation-area';
import LiveHeader from '../live/live-header';
import LiveBigPlays from '../live/live-big-plays';
import DebugMenu from './debug-menu';

const stubData = {
  watching: {
    sport: 'nba',
    contestId: 2,
    opponentLineupId: null, // Null if you don't want to see the opponents overall-stats
  },
  currentEvent: null,
  eventsMultipart: {},
  contest: {
    name: 'Debug Contest',
    potentialWinnings: 10,
    rank: 2,
    isLoading: false,
  },
  uniqueLineups: {
    lineups: [],
  },
  myLineupInfo: {
    name: 'MyLineup',
    fp: 0,
    id: 2,
    isLoading: false,
    potentialWinnings: 10,
    rank: 1,
    timeRemaining: {
      decimal: 1,
      duration: 50,
    },
  },
  opponentLineup: {
    name: 'OpponentLineup',
    fp: 0,
    id: 3,
    rank: 2,
    timeRemaining: {
      decimal: 1,
      duration: 50,
    },
    isLoading: false,
  },
  selectLineup: () => { },
};

/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
const mapStateToProps = (state) => ({
  currentEvent: state.events.currentEvent,
  showEventResult: state.events.showEventResult,
  bigEvents: state.events.bigEvents,
});


export default connect(mapStateToProps)(React.createClass({
  propTypes: {
    currentEvent: React.PropTypes.object,
    bigEvents: React.PropTypes.array,
    showEventResult: React.PropTypes.bool,
  },

  getInitialState() {
    return {};
  },

  render() {
    const { eventsMultipart, watching } = stubData;
    const { currentEvent, bigEvents, showEventResult } = this.props;

    return (
      <section className="debug-live-animations">
        <DebugMenu />
        <div className="live">
          <section className="live__venues">
            <div className="live__venues-inner">
              <LiveHeader
                currentEvent={currentEvent}
                showEventResult={showEventResult}
                contest={stubData.contest}
                lineups={stubData.uniqueLineups.lineups}
                myLineup={stubData.myLineupInfo}
                opponentLineup={stubData.opponentLineup}
                selectLineup={stubData.selectLineup}
                watching={stubData.watching}
              />
              <LiveAnimationArea {...{ watching, currentEvent, eventsMultipart }} />
            </div>
          </section>
          <LiveBigPlays queue={bigEvents || []} />
        </div>
      </section>
    );
  },
}));
