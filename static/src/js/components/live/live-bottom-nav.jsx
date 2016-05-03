import React from 'react';

import * as AppActions from '../../stores/app-state-store';


/**
 * Bottom nav for the live section, changes based on watching contest vs lineup
 */
const LiveBottomNav = React.createClass({
  propTypes: {
    hasContest: React.PropTypes.bool.isRequired,
  },

  toggleStandings() {
    AppActions.toggleLiveRightPane('appstate--live-standings-pane--open');
  },

  toggleContests() {
    AppActions.toggleLiveRightPane('appstate--live-contests-pane--open');
  },

  render() {
    let classNames = 'live-right-pane-nav live-right-pane-nav--';
    let toggleStandings;

    if (this.props.hasContest) {
      classNames += 'contest';
      toggleStandings = (
        <div className="live-right-pane-nav__view-standings" onClick={this.toggleStandings}>
          <span>View Standings &amp; Ownership</span>
        </div>
      );

    // otherwise watching lineup
    } else {
      classNames += 'lineup';
    }

    return (
      <div className={ classNames }>
        <div className="live-right-pane-nav__view-contests" onClick={this.toggleContests}>
          <span>View Contests</span>
        </div>
        { toggleStandings }
      </div>
    );
  },
});

export default LiveBottomNav;
