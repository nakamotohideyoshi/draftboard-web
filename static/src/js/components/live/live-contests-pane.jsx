import React from 'react';
import map from 'lodash/map';
import size from 'lodash/size';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { humanizeCurrency } from '../../lib/utils/currency';
import { updateWatchingAndPath } from '../../actions/watching.js';
import * as AppActions from '../../stores/app-state-store';
import LiveContestsPaneItem from './live-contests-pane-item';


/*
 * Map Redux actions to React component properties
 * @param  {function} dispatch The dispatch method to pass actions into
 * @return {object}            All of the methods to map to the component, wrapped in 'action' key
 */
const mapDispatchToProps = (dispatch) => ({
  actions: bindActionCreators({
    updateWatchingAndPath,
  }, dispatch),
});

/**
 * When `View Contests` element is clicked, open side pane to show
 * a user's current contests for that lineup.
 */
export const LiveContestsPane = React.createClass({

  propTypes: {
    actions: React.PropTypes.object.isRequired,
    lineup: React.PropTypes.object.isRequired,
    openOnStart: React.PropTypes.bool.isRequired,
    watching: React.PropTypes.object.isRequired,
  },

  componentDidMount() {
    if (this.props.openOnStart) AppActions.addClass('appstate--live-contests-pane--open');
  },

  viewContest(contestId) {
    const { actions, watching } = this.props;
    const path = `/live/${watching.sport}/lineups/${watching.myLineupId}/contests/${contestId}/`;
    const changedFields = {
      draftGroupId: watching.draftGroupId,
      myLineupId: watching.myLineupId,
      contestId,
    };

    actions.updateWatchingAndPath(path, changedFields);

    // open up the standings pane, fade out contests
    AppActions.addClass('appstate--live-contests-pane--faded-out');
  },

  renderContests() {
    const { lineup } = this.props;

    return map(lineup.contestsStats, (contest) => (
      <LiveContestsPaneItem
        contest={contest}
        onItemClick={this.viewContest}
        key={contest.id}
      />
    ));
  },

  render() {
    const { contestsStats, totalBuyin, potentialWinnings } = this.props.lineup;

    return (
      <div className="live-contests-pane live-pane live-pane--right">
        <div className="live-pane__content">
          <h2>
            My Contests

            <div className="stats">
              <div className="num-contest">
                {size(contestsStats)} <span>Contests</span>
              </div>

              <div className="profit">
                <div className="fees">
                  {humanizeCurrency(totalBuyin)} Fees
                </div>
                {" "} / {" "}
                <div className="earnings">
                  Winning
                  {" "}
                  <span>{humanizeCurrency(potentialWinnings)}</span>
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

// Wrap the component to inject dispatch and selected state into it.
export default connect(
  () => ({}),
  mapDispatchToProps
)(LiveContestsPane);
