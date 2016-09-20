import React from 'react';
import forEach from 'lodash/forEach';
import size from 'lodash/size';

import NavScoreboardFilters from './nav-scoreboard-filters';
import NavScoreboardGamesList from './nav-scoreboard-games-list';
import NavScoreboardLineupsList from './nav-scoreboard-lineups-list';
import NavScoreboardLoggedOutInfo from './nav-scoreboard-logged-out-info';
import NavScoreboardLogo from './nav-scoreboard-logo';
import NavScoreboardMenu from './nav-scoreboard-menu';
import NavScoreboardReplayerData from './nav-scoreboard-replayer-data';
import NavScoreboardSeparator from './nav-scoreboard-separator';
import NavScoreboardSlider from './nav-scoreboard-slider';
import NavScoreboardUserInfo from './nav-scoreboard-user-info';

import { TYPE_SELECT_GAMES, TYPE_SELECT_LINEUPS } from './nav-scoreboard-const';

/*
 * The overarching component for the scoreboard spanning the top of the site.
 *
 * Most important thing to glean from this comment is that this component is the
 * one that loads all data for the live and scoreboard redux substores!
 */
const NavScoreboardStatic = React.createClass({
  propTypes: {
    user: React.PropTypes.object.isRequired,
    sportsSelector: React.PropTypes.object.isRequired,
    myCurrentLineupsSelector: React.PropTypes.object.isRequired,
    cashBalance: React.PropTypes.oneOfType([
      React.PropTypes.string,
      React.PropTypes.number,
    ]),
  },

  getInitialState() {
    return {
      // Selected option string. SEE: `getSelectOptions`
      selectedOption: null,

      // Selected option type. See type constants above.
      selectedType: null,

      // Selected option key. Subtype from the main type.
      // Competition from games and null for lineups.
      selectedKey: null,
    };
  },

  /**
   * Get the options for `NavScoreboardFilters` select menu.
   * @return {Array} options key-value pairs
   */
  getSelectOptions() {
    const options = [];

    forEach(this.props.sportsSelector.types, (sport) => {
      // Make sure it doesn't break if the sport has no games.
      let count = 0;
      if (this.props.sportsSelector[sport].gameIds) {
        count = this.props.sportsSelector[sport].gameIds.length;
      }

      // Don't show inactive sports.
      if (count > 0) {
        options.push({
          option: `${sport} games`,
          type: TYPE_SELECT_GAMES,
          key: sport,
          count,
        });
      }
    });

    // add in lineups if user is logged in
    if (this.props.user.username !== '') {
      options.push({
        option: 'MY LINEUPS',
        type: TYPE_SELECT_LINEUPS,
        key: 'LINEUPS',
        count: size(this.props.myCurrentLineupsSelector),
      });
    }

    return options;
  },

  /**
   * Handle `NavScoreboardFilters` select menu change.
   * @param {String} selectedOption Name of the selected option
   * @param {String} selectedType Type of the selected item
   * @param {String} selectedKey Key of the selected item type
   * @return {Object} options key-value pairs
   */
  handleChangeSelection(selectedOption, selectedType, selectedKey) {
    this.setState({ selectedOption, selectedType, selectedKey });
  },

  /**
   * Render slider contents based on selected filter.
   */
  renderSliderContent() {
    if (this.state.selectedType === TYPE_SELECT_LINEUPS) {
      if (Object.keys(this.props.myCurrentLineupsSelector).length === 0) return null;

      return <NavScoreboardLineupsList lineups={this.props.myCurrentLineupsSelector} />;
    } else if (this.state.selectedType === TYPE_SELECT_GAMES) {
      if (!this.props.sportsSelector[this.state.selectedKey].gameIds) return null;

      return (
        <NavScoreboardGamesList
          sport={this.props.sportsSelector[this.state.selectedKey]}
          games={this.props.sportsSelector.games}
        />
      );
    }

    return null;
  },

  render() {
    const { username } = this.props.user;
    let userInfo;
    let replayerData;
    let filters;
    let slider;

    if (size(this.props.sportsSelector.games) > 0) {
      filters = (
        <NavScoreboardFilters
          selected={this.state.selectedOption}
          options={this.getSelectOptions()}
          onChangeSelection={this.handleChangeSelection}
        />
      );
      slider = (
        <NavScoreboardSlider type={this.state.selectedOption}>
          {this.renderSliderContent()}
        </NavScoreboardSlider>
      );
    }

    if (this.props.user.username !== '') {
      userInfo = (
        <NavScoreboardUserInfo name={username} balance={this.props.cashBalance} />
      );
    } else {
      userInfo = (
        <NavScoreboardLoggedOutInfo />
      );
    }

    if (window.dfs.replayerTimeDelta > 0) {
      replayerData = (<NavScoreboardReplayerData />);
    }

    return (
      <div className="inner">
        <NavScoreboardMenu />
        <NavScoreboardSeparator half />
        { userInfo }
        <NavScoreboardSeparator />
        { filters }
        { slider }
        <NavScoreboardLogo />
        { replayerData }
      </div>
    );
  },
});

export default NavScoreboardStatic;
