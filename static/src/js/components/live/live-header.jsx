import * as AppActions from '../../stores/app-state-store';
import LiveOverallStats from './live-overall-stats';
import React from 'react';


/**
 * Return the header section of the live page, including the lineup/contest title and overall stats
 */
const LiveHeader = React.createClass({

  propTypes: {
    changePathAndMode: React.PropTypes.func.isRequired,
    contest: React.PropTypes.object.isRequired,
    myLineup: React.PropTypes.object.isRequired,
    opponentLineup: React.PropTypes.object.isRequired,
    watching: React.PropTypes.object.isRequired,
  },

  /**
   * Used to close the current contest. Sets up parameters to then call props.changePathAndMode()
   */
  returnToLineup() {
    const watching = this.props.watching;
    const path = `/live/${watching.sport}/lineups/${watching.myLineupId}/`;
    const changedFields = {
      opponentLineupId: null,
      contestId: null,
    };

    this.props.changePathAndMode(path, changedFields);

    // open the standings pane back up
    AppActions.addClass('appstate--live-contests-pane--open');
  },

  /**
   * Typical react render method. What's interesting here is that we default to when there's just a lineup, then
   * modify the DOM elements if we're viewing a contest and/or an opponent.
   */
  render() {
    const { myLineup, contest, opponentLineup, watching } = this.props;

    // set all needed variables, and default them to lineup only
    let closeContest;
    let opponentStats;
    let primary = myLineup.name;
    let secondary;
    let statsVs;
    let hasContest = false;


    // if watching a contest, then update the titles and ensure the overall stats are contest-based
    if (watching.contestId !== null && !contest.isLoading) {
      hasContest = true;
      primary = contest.name;
      secondary = myLineup.name;
      closeContest = (
        <span className="live-scoreboard__close" onClick={this.returnToLineup}></span>
      );


      // if watching an opponent, then add in second overall stats and update the titles
      if (watching.opponentLineupId !== null && !opponentLineup.isLoading) {
        let username = '';
        if (opponentLineup.hasOwnProperty('user')) {
          username = opponentLineup.user.username;
        // if villian, use name
        } else if (opponentLineup.id === 1) {
          username = opponentLineup.name;
        }

        secondary = (
          <div>
            {myLineup.name} <span className="vs">vs</span> {username}
          </div>
        );
        statsVs = (
          <div className="live-overall-stats__vs">vs</div>
        );
        opponentStats = (
          <LiveOverallStats
            contest={contest}
            hasContest
            lineup={opponentLineup}
            whichSide="opponent"
          />
        );
      }
    }

    return (
      <header className="cmp-live__scoreboard live-scoreboard">
        <h2 className="live-scoreboard__lineup-name">
          {secondary}
        </h2>
        <h1 className="live-scoreboard__contest-name">
          {primary}
          {closeContest}
        </h1>

        <LiveOverallStats
          contest={contest}
          lineup={myLineup}
          hasContest={hasContest}
          whichSide="mine"
        />

        {statsVs}
        {opponentStats}
      </header>
    );
  },
});

export default LiveHeader;
