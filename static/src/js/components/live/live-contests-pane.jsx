import LiveContestsPaneItem from './live-contests-pane-item';
import map from 'lodash/map';
import merge from 'lodash/merge';
import React from 'react';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { generateBlockNameWithModifiers } from '../../lib/utils/bem';
import { updateWatchingAndPath } from '../../actions/watching.js';

// assets
require('../../../sass/blocks/live/live-contests-pane.scss');


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

  getInitialState() {
    return {
      modifiers: [],
    };
  },

  componentWillMount() {
    const state = merge({}, this.state);

    if (this.props.watching.opponentLineupId !== null) {
      state.modifiers = ['opponent-mode'];

      this.setState(state);
    }
  },

  // close the window when in opponent mode
  componentWillReceiveProps(nextProps) {
    const state = merge({}, this.state);
    // const { actions, watching } = this.props;

    if (nextProps.watching.opponentLineupId !== this.props.watching.opponentLineupId) {
      if (nextProps.watching.opponentLineupId === null) {
        state.modifiers = [];
      }

      if (nextProps.watching.opponentLineupId !== null) {
        state.modifiers = ['opponent-mode'];
      }
    }

    this.setState(state);
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
  },

  backToContestsPane() {
    const { actions, watching } = this.props;
    const path = `/live/${watching.sport}/lineups/${watching.myLineupId}/`;
    const changedFields = {
      contestId: null,
    };

    actions.updateWatchingAndPath(path, changedFields);
  },

  renderContests() {
    const { lineup, watching } = this.props;

    let index = 0;
    const contestsSize = Object.keys(lineup.contestsStats).length;
    return map(lineup.contestsStats, (contest) => {
      index++;
      const modifiers = [];
      if (watching.contestId === contest.id) modifiers.push('active');

      return (
        <LiveContestsPaneItem
          contest={contest}
          contestsSize={contestsSize}
          index={index}
          backToContestsPane={this.backToContestsPane}
          onItemClick={this.viewContest}
          key={contest.id}
          modifiers={modifiers}
        />
      );
    });
  },

  render() {
    const block = 'live-contests-pane';
    const classNames = generateBlockNameWithModifiers(block, this.state.modifiers);

    return (
      <ul className={classNames}>
        {this.renderContests()}
      </ul>
    );
  },
});

// Wrap the component to inject dispatch and selected state into it.
export default connect(
  () => ({}),
  mapDispatchToProps
)(LiveContestsPane);
