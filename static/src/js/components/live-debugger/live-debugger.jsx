import { connect } from 'react-redux';
import React from 'react';
import LiveAnimationArea from '../live/live-animation-area';
import LiveHeader from '../live/live-header';
import LiveBigPlays from '../live/live-big-plays';
import LiveStandingsPane from '../live/live-standings-pane';
import DebugMenu from './debug-menu';

require('../../../sass/blocks/live-debugger.scss');

const stubMyLineup = {
  id: 2,
  name: 'My Lineup',
  fp: 5,
  isLoading: false,
  potentialWinnings: 10,
  rank: 1,
  timeRemaining: {
    decimal: 0.91,
    duration: 50,
  },
};

const stubOppLineup = {
  id: 3,
  name: 'Opponent Lineup',
  fp: 20,
  rank: 2,
  potentialWinnings: 10,
  timeRemaining: {
    decimal: 0.91,
    duration: 50,
  },
  isLoading: false,
};

const stubOtherLineup = {
  id: 4,
  name: 'Other Lineup',
  fp: 15,
  rank: 3,
  potentialWinnings: 10,
  timeRemaining: {
    decimal: 0.91,
    duration: 50,
  },
  isLoading: false,
};

const stubDebugLineup = {
  id: 5,
  name: 'Debug Lineup',
  fp: 50,
  rank: 4,
  potentialWinnings: 10,
  timeRemaining: {
    decimal: 0.91,
    duration: 50,
  },
  isLoading: false,
};

const stubContest = {
  name: 'Debug Contest',
  potentialWinnings: 10,
  rank: 2,
  isLoading: false,
  hasLineupsUsernames: true,
  lineups: {
    [stubMyLineup.id]: stubMyLineup,
    [stubOppLineup.id]: stubOppLineup,
    [stubOtherLineup.id]: stubOtherLineup,
    [stubDebugLineup.id]: stubDebugLineup,
  },
  lineupsUsernames: {
    [stubMyLineup.id]: stubMyLineup.name,
    [stubOppLineup.id]: stubOppLineup.name,
    [stubOtherLineup.id]: stubOtherLineup.name,
    [stubDebugLineup.id]: stubDebugLineup.name,
  },
  rankedLineups: [
    stubMyLineup.id,
    stubOppLineup.id,
    stubOtherLineup.id,
    stubDebugLineup.id,
  ],
  prize: {
    info: {
      buyin: 1,
      payout_spots: 3,
      pk: 0,
      prize_pool: 0,
      ranks: [{
        category: 'cash',
        rank: 1,
        value: 1.8,
      }],
    },
  },
};

const stubAvailableLineups = [stubMyLineup, stubOppLineup, stubOtherLineup, stubDebugLineup];

const stubData = {
  watching: {
    sport: 'nba',
    contestId: 2,
    myLineupId: stubMyLineup.id,
    opponentLineupId: 3, // Null if you don't want to see the opponents overall-stats
  },
  currentEvent: null,
  eventsMultipart: {},
  contest: stubContest,
  uniqueLineups: {
    lineups: stubAvailableLineups,
  },
  myLineupInfo: stubMyLineup,
  opponentLineup: stubOppLineup,
  selectLineup: () => { },
};

/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
const mapStateToProps = (state) => ({
  currentEvent: state.events.currentEvent,
  bigEvents: state.events.bigEvents,
});


export default connect(mapStateToProps)(React.createClass({
  propTypes: {
    currentEvent: React.PropTypes.object,
    bigEvents: React.PropTypes.array,
  },

  getInitialState() {
    return {};
  },

  componentWillMount() {
    window.is_debugging_live_animation = true;
  },

  render() {
    const { eventsMultipart, watching, contest } = stubData;
    const { currentEvent, bigEvents } = this.props;

    return (
      <div className="live">
        <DebugMenu />
        <section className="live__venues">
          <LiveHeader
            {...{ contest, currentEvent, watching }}
            lineups={stubData.uniqueLineups.lineups}
            myLineup={stubData.myLineupInfo}
            opponentLineup={stubData.opponentLineup}
            selectLineup={stubData.selectLineup}
          />
          <LiveAnimationArea {...{ currentEvent, eventsMultipart, watching }} />
          <LiveStandingsPane {...{ contest, watching }} />
        </section>
        <LiveBigPlays queue={bigEvents || []} />
      </div>
    );
  },
}));
