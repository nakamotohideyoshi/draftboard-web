import React from 'react';
import { map as _map } from 'lodash';

import * as AppActions from '../../stores/app-state-store';
import LiveContestsPaneItem from './live-contests-pane-item';


/**
 * When `View Contests` element is clicked, open side pane to show
 * a user's current contests for that lineup.
 */
const LiveContestsPane = React.createClass({

  propTypes: {
    changePathAndMode: React.PropTypes.func.isRequired,
    lineup: React.PropTypes.object.isRequired,
    openOnStart: React.PropTypes.bool.isRequired,
    watching: React.PropTypes.object.isRequired,
  },

  componentWillMount() {
    if (this.props.openOnStart) {
      AppActions.addClass('appstate--live-contests-pane--open');
    }
  },

  viewContest(contestId) {
    const watching = this.props.watching;
    const path = `/live/${watching.sport}/lineups/${watching.myLineupId}/contests/${contestId}/`;
    const changedFields = {
      draftGroupId: watching.draftGroupId,
      myLineupId: watching.myLineupId,
      contestId,
    };

    this.props.changePathAndMode(path, changedFields);
    this.closePane();
  },

  closePane() {
    AppActions.removeClass('appstate--live-contests-pane--open');
  },

  renderContests() {
    const lineup = this.props.lineup;

    return _map(lineup.contestsStats, (contest) => (
      <LiveContestsPaneItem
        contest={contest}
        onItemClick={this.viewContest}
        key={contest.id}
      />
    ));
  },

  render() {
    const { lineup } = this.props;
    const fees = lineup.totalBuyin;
    const winnings = lineup.potentialWinnings;

    return (
      <div className="live-contests-pane live-pane live-pane--right">
        <div className="live-pane__content">
          <h2>
            My Contests

            <div className="stats">
              <div className="num-contest">
                18 <span>Contests</span>
              </div>

              <div className="profit">
                <div className="fees">
                  ${fees} Fees
                </div>
                {" "} / {" "}
                <div className="earnings">
                  Winning
                  {" "}
                  <span>${winnings}</span>
                </div>
              </div>
            </div>
          </h2>

          <div className="live-contests-pane__list">
            <ul className="live-contests-pane__list__inner">
              {this.renderContests()}
            </ul>
          </div>
        </div>
        <div className="live-pane__left-shadow" />

        <div className="live-contests-pane__view-contest" onClick={this.viewContest} />
      </div>
    );
  },
});

export default LiveContestsPane;
