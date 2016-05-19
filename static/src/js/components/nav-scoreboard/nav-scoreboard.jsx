import Pusher from 'pusher-js';
import React from 'react';
import { forEach as _forEach } from 'lodash';
import { Provider, connect } from 'react-redux';
import { size as _size } from 'lodash';

import errorHandler from '../../actions/live-error-handler';
import log from '../../lib/logging';
import renderComponent from '../../lib/render-component';
import store from '../../store';

import { fetchEntriesIfNeeded } from '../../actions/entries';
import { fetchSportsIfNeeded } from '../../actions/sports';
import { myCurrentLineupsSelector } from '../../selectors/current-lineups';
import { removeUnusedContests } from '../../actions/live-contests';
import { removeUnusedDraftGroups } from '../../actions/live-draft-groups';
import { sportsSelector } from '../../selectors/sports';
import { updateGameTeam } from '../../actions/sports';
import { updateGameTime } from '../../actions/sports';

import NavScoreboardFilters from './nav-scoreboard-filters';
import NavScoreboardGamesList from './nav-scoreboard-games-list';
import NavScoreboardLineupsList from './nav-scoreboard-lineups-list';
import NavScoreboardLoggedOutInfo from './nav-scoreboard-logged-out-info';
import NavScoreboardLogo from './nav-scoreboard-logo';
import NavScoreboardMenu from './nav-scoreboard-menu';
import NavScoreboardSeparator from './nav-scoreboard-separator';
import NavScoreboardSlider from './nav-scoreboard-slider';
import NavScoreboardUserInfo from './nav-scoreboard-user-info';
import PusherData from '../site/pusher-data';

import { TYPE_SELECT_GAMES, TYPE_SELECT_LINEUPS } from './nav-scoreboard-const';


/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
const mapStateToProps = (state) => ({
  cashBalance: state.user.cashBalance.amount,
  myCurrentLineupsSelector: myCurrentLineupsSelector(state),
  sportsSelector: sportsSelector(state),
});

/*
 * The overarching component for the scoreboard spanning the top of the site.
 *
 * Most important thing to glean from this comment is that this component is the one that loads all data for the live
 * and scoreboard redux substores!
 */
const NavScoreboard = React.createClass({

  propTypes: {
    cashBalance: React.PropTypes.string,
    myCurrentLineupsSelector: React.PropTypes.object.isRequired,
    dispatch: React.PropTypes.func.isRequired,
    sportsSelector: React.PropTypes.object.isRequired,
  },


  getDefaultProps() {
    return {
      cashBalance: `$${window.dfs.user.cashBalance}`,
    };
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

      // whether the user is logged in or not, useful for parity checks
      user: window.dfs.user,

      // whether or not we are on the live page (determines what data to load)
      isLivePage: window.location.pathname.substring(0, 6) === '/live/',
    };
  },

  /**
   * Pull in relevant sports and relevant entries (entries getting lineup data)
   * We separate into different try/catches so we can debug with the error message
   */
  componentWillMount() {
    const defaultMessage = 'Our support team has been alerted of this error and will fix immediately.';

    try {
      this.props.dispatch(fetchSportsIfNeeded());
    } catch (e) {
      this.props.dispatch(errorHandler(e, `#AJSDFJWI ${defaultMessage}`));
    }

    // if the user is logged in
    if (this.state.user.username !== '' && window.location.pathname !== '/live/') {
      try {
        this.props.dispatch(fetchEntriesIfNeeded());
      } catch (e) {
        this.props.dispatch(errorHandler(e, `#JASDFJIE ${defaultMessage}`));
      }
    }

    this.startListening();
  },

  /**
   * Get the options for `NavScoreboardFilters` select menu.
   * @return {Array} options key-value pairs
   */
  getSelectOptions() {
    const options = [];

    _forEach(this.props.sportsSelector.types, (sport) => {
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
    if (this.state.user.username !== '') {
      options.push({
        option: 'MY LINEUPS',
        type: TYPE_SELECT_LINEUPS,
        key: 'LINEUPS',
        count: _size(this.props.myCurrentLineupsSelector),
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

  /*
   * Start up Pusher listeners to the necessary channels and events
   */
  listenToSockets() {
    // let the live page do game score calls
    if (this.state.isLivePage === true) {
      return;
    }

    log.info('NavScoreboard.listenToSockets()');

    // NOTE: this really bogs down your console
    // Pusher.log = function(message) {
    //   if (window.console && window.console.log) {
    //     window.console.log(message);
    //   }
    // };

    const pusher = new Pusher(window.dfs.user.pusher_key, {
      encrypted: true,
    });

    // used to separate developers into different channels, based on their django settings filename
    const channelPrefix = window.dfs.user.pusher_channel_prefix.toString();

    const boxscoresChannel = pusher.subscribe(`${channelPrefix}boxscores`);
    boxscoresChannel.bind('team', (eventData) => {
      if (this.props.sportsSelector.games.hasOwnProperty(eventData.game__id) &&
          eventData.hasOwnProperty('points')
      ) {
        this.props.dispatch(updateGameTeam(
          eventData.game__id,
          eventData.id,
          eventData.points
        ));
      }
    });
    boxscoresChannel.bind('game', (eventData) => {
      if (this.props.sportsSelector.games.hasOwnProperty(eventData.id) &&
          eventData.hasOwnProperty('clock')
      ) {
        this.props.dispatch(updateGameTime(
          eventData.id,
          eventData
        ));
      }
    });
  },

  /**
   * Internal method to start listening to pusher and poll for updates
   */
  startListening() {
    this.listenToSockets();
    this.startParityChecks();
    this.removeExpiredSubstoreObjects();
  },

  /**
   * Helper method to aggregate all of the methods needed to remove expired objects within Redux.
   * Is run once per page load.
   */
  removeExpiredSubstoreObjects() {
    this.props.dispatch(removeUnusedContests());
    this.props.dispatch(removeUnusedDraftGroups());
  },

  /**
   * Periodically override the redux state with server data, to ensure that we have up to date data in case we missed
   * a Pusher call here or there. In time the intervals will increase, as we gain confidence in the system.
   */
  startParityChecks() {
    // whether we are logged in or not, we always need to check whether to update sports and draftgroups
    // check every few seconds, and if expired (which happens after 10 minutes), then they will fetch
    const parityChecks = {
      sports: window.setInterval(() => this.props.dispatch(fetchSportsIfNeeded()), 5000),
    };

    // add the checsk to the state in case we need to clearInterval in the future
    this.setState({ boxScoresIntervalFunc: parityChecks });
  },

  /**
   * Render slider contents based on selected filter.
   */
  renderSliderContent() {
    if (this.state.selectedType === TYPE_SELECT_LINEUPS) {
      return <NavScoreboardLineupsList lineups={this.props.myCurrentLineupsSelector} />;
    } else if (this.state.selectedType === TYPE_SELECT_GAMES) {
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
    const { username } = window.dfs.user;
    let userInfo;
    let filters;
    let slider;

    if (_size(this.props.sportsSelector.games) > 0) {
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

    if (this.state.user.username !== '') {
      userInfo = (
        <NavScoreboardUserInfo name={username} balance={this.props.cashBalance} />
      );
    } else {
      userInfo = (
        <NavScoreboardLoggedOutInfo />
      );
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
        <PusherData />
      </div>
    );
  },
});

// Wrap the component to inject dispatch and selected state into it.
const NavScoreboardConnected = connect(mapStateToProps)(NavScoreboard);

// Uses the Provider to have redux state
renderComponent(
  <Provider store={store}>
    <NavScoreboardConnected />
  </Provider>,
  '.cmp-nav-scoreboard'
);
