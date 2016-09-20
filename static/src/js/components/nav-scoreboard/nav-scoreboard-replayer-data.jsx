import React from 'react';
import { dateNow } from '../../lib/utils';

// assets
require('../../../sass/blocks/nav-scoreboard/nav-scoreboard-replayer-data.scss');


/**
 * Stateless component that houses replayer data when needed
 *
 * @param  {object} props React props
 * @return {jsx}          JSX of component
 */
const NavScoreboardReplayerData = React.createClass({
  getInitialState() {
    return { replayerSeconds: window.dfs.replayerTimeDelta };
  },

  // update every second
  componentDidMount() {
    this.timer = setInterval(this.tick, 1000);
  },

  componentWillUnmount() {
    clearInterval(this.timer);
  },

  // advance by one second
  tick() {
    this.setState({ currentDate: dateNow() });
  },

  render() {
    const replayerDate = new Date(this.state.currentDate);

    return (
      <div className="nav-scoreboard-replayer-data">
        { replayerDate.toString() }
      </div>
    );
  },
});

export default NavScoreboardReplayerData;
