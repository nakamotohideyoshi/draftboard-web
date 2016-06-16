import * as ReactRedux from 'react-redux';
import Cookies from 'js-cookie';
import debounce from 'lodash/debounce';
import map from 'lodash/map';
import React from 'react';
import request from 'superagent';

import * as AppActions from '../../stores/app-state-store';
import LivePMRProgressBar from './live-pmr-progress-bar';
import { bindActionCreators } from 'redux';
import { fetchLineupUsernames } from '../../actions/lineup-usernames';
import { humanizeFP } from '../../actions/sports';
import { SPORT_CONST } from '../../actions/sports.js';
import { updateLiveMode, updateWatchingAndPath } from '../../actions/watching.js';

const STANDINGS_TAB = 'standings';
const OWNERSHIP_TAB = 'ownership';


/*
 * Map Redux actions to React component properties
 * @param  {function} dispatch The dispatch method to pass actions into
 * @return {object}            All of the methods to map to the component, wrapped in 'action' key
 */
const mapDispatchToProps = (dispatch) => ({
  actions: bindActionCreators({
    fetchLineupUsernames,
    updateLiveMode,
    updateWatchingAndPath,
  }, dispatch),
});

/**
 * When `View Contests` element is clicked, open side pane to show
 * a user's current contests for that lineup.
 */
export const LiveStandingsPane = React.createClass({

  propTypes: {
    actions: React.PropTypes.object.isRequired,
    lineups: React.PropTypes.object.isRequired,
    contest: React.PropTypes.object.isRequired,
    openOnStart: React.PropTypes.bool.isRequired,
    rankedLineups: React.PropTypes.array.isRequired,
    watching: React.PropTypes.object.isRequired,
  },

  getInitialState() {
    return {
      page: 1,                             // Current page number starting from 1.
      perPage: 10,                         // Items per page.
      searchValue: '',                     // Search input value.
      searchResults: [],                   // Results of the search.
      searchPlaceholder: 'Search Users',   // Search field placeholder.
      currentTab: STANDINGS_TAB,           // Currently shown tab.
      playersSortKey: null,                // Key to sort players.
      playersSortAsc: false,               // Is players sort ascending or descending.
      playersWatched: [],                  // Watched players.
    };
  },

  componentWillMount() {
    if (this.props.openOnStart) AppActions.addClass('appstate--live-standings-pane--open');

    if (this.props.watching.villainLineup) {
      this.setState({ playersWatched: this.props.watching.villainLineup });
    }
  },

  componentDidMount() {
    // this.props.actions.fetchLineupUsernames(this.props.watching.contestId)
    this.handleSearchByUsername = debounce(this.handleSearchByUsername, 150);
  },

  /**
   * Get list data that should be rendered in the current tab.
   * @return {Array}
   */
  getListData() {
    let data;

    if (this.state.currentTab === STANDINGS_TAB) {
      const lineups = this.props.lineups;
      const rankedLineups = this.props.rankedLineups;
      data = map(rankedLineups, (lineupId) => lineups[lineupId]);
    } else {
      data = this.props.contest.playersOwnership.all.slice();

      if (this.state.playersSortKey) {
        const key = this.state.playersSortKey;
        const asc = this.state.playersSortAsc;

        data.sort((p, n) => {
          let r;

          if (key === 'pmr') {
            r = p.stats.decimalRemaining - n.stats.decimalRemaining;
          } else if (key === 'pts') {
            r = p.stats.fp - n.stats.fp;
          } else if (key === 'owned') {
            r = p.ownershipPercent - n.ownershipPercent;
          }

          if (!asc) r *= -1;

          return r;
        });
      }
    }

    if (this.state.searchValue !== '') {
      if (this.state.currentTab === STANDINGS_TAB) {
        data = data.filter(p => this.state.searchResults.indexOf(p.id) !== -1);
      } else {
        const s = this.state.searchValue;
        data = data.filter(p => p.name.toLowerCase().indexOf(s.toLowerCase()) !== -1);
      }
    }

    return data;
  },

  /**
   * Get the maximum page number for data in #getListData().
   * @return {Number}
   */
  getMaxPage() {
    return Math.ceil(this.getListData().length / this.state.perPage);
  },

  handleViewOwnership() {
    this.setState({
      page: 1,
      searchValue: '',
      searchResults: [],
      searchPlaceholder: 'Search Players',
      currentTab: OWNERSHIP_TAB,
      playersSortKey: null,
      playersSortAsc: false,
    });
  },

  handleViewStandings() {
    this.setState({
      page: 1,
      searchValue: '',
      searchResults: [],
      searchPlaceholder: 'Search Users',
      currentTab: STANDINGS_TAB,
    });
  },

  handleViewNextPage() {
    const maxPage = this.getMaxPage();
    const page = Math.min(this.state.page + 1, maxPage);
    this.setState({ page });
  },

  handleViewPrevPage() {
    const page = Math.max(this.state.page - 1, 1);
    this.setState({ page });
  },

  /**
   * Used to view an opponent lineup. Sets up parameters to then call props.updateWatchingAndPath()
   */
  handleViewOpponentLineup(opponentLineupId) {
    const { actions, watching } = this.props;
    const lineupUrl = `/live/${watching.sport}/lineups/${watching.myLineupId}`;
    const path = `${lineupUrl}/contests/${watching.contestId}/opponents/${opponentLineupId}/`;
    const changedFields = {
      opponentLineupId,
    };

    actions.updateWatchingAndPath(path, changedFields);
    AppActions.toggleLiveRightPane('appstate--live-standings-pane--open');
  },

  handleFocusSearch() {
    this.setState({
      searchValue: '',
    });

    if (this.refs.search) {
      this.refs.search.focus();
    }
  },

  handleSearchTermChanged() {
    this.setState({ searchValue: this.refs.search.value });

    if (this.state.currentTab === STANDINGS_TAB) {
      this.handleSearchByUsername();
    }
  },

  handleSearchByUsername() {
    const params = {
      contest_id: this.props.watching.contestId,
      search_str: this.state.searchValue,
    };

    // TODO: report errors
    return request
      .post('/api/lineup/usernames/')
      .send(params)
      .set({ 'X-CSRFToken': Cookies.get('csrftoken') })
      .set({ 'X-REQUESTED-WITH': 'XMLHttpRequest' })
      .set('Accept', 'application/json')
      .end((err, res) => {
        if (!err) {
          let data;
          try {
            data = JSON.parse(res.text);
          } catch (e) {
            data = [];
          }

          this.setState({ searchResults: data.map((l) => l.id) });
        } else {
          this.setState({ searchResults: [] });
        }
      });
  },

  handleSortPlayers(key) {
    if (key !== 'pmr' && key !== 'pts' && key !== 'owned') return;

    if (this.state.playersSortKey === key) {
      this.setState({
        playersSortAsc: !this.state.playersSortAsc,
      });
    } else {
      this.setState({
        playersSortKey: key,
        playersSortAsc: false,
      });
    }
  },

  handleToggleWatchPlayer(id) {
    let playersWatched = this.state.playersWatched.slice();

    const game = SPORT_CONST[this.props.watching.sport];
    const maxPlayers = game ? game.players : 10;

    if (playersWatched.indexOf(id) !== -1) {
      playersWatched = playersWatched.filter(i => i !== id);
    } else if (playersWatched.length < maxPlayers) {
      playersWatched.push(id);
    } else {
      return;
    }

    if (playersWatched.length === maxPlayers) {
      this.props.actions.updateLiveMode({ villainLineup: playersWatched });
    }

    this.setState({ playersWatched });
  },

  handleWatchVillainLineup() {
    // NOTE: 1 is a special lineup id indicating selected villain lineup.
    this.handleViewOpponentLineup(1);
  },

  backToContestsPane() {
    const { actions, watching } = this.props;
    const path = `/live/${watching.sport}/lineups/${watching.myLineupId}/`;
    const changedFields = {
      contestId: null,
    };

    // immediately animate in contest pane
    AppActions.removeClass('appstate--live-standings-pane--open');
    AppActions.addClass('appstate--live-contests-pane--open');

    // hacky! match time with css animation
    setTimeout(() => {
      actions.updateWatchingAndPath(path, changedFields);
    }, 230);
  },

  renderHeader() {
    const { contest } = this.props;
    const { amount, percent } = contest.potentialWinnings;

    let moneyLineClass = 'live-moneyline';

    if (percent < contest.percentageCanWin) {
      moneyLineClass += ' live-moneyline--is-losing';
    }

    return (
      <div className="live-standings-pane__header">
        <div className="stats">
          <div className="title">{contest.name}</div>
          <div className="profit">
            <div className="fees">
              ${contest.buyin} Fees
            </div>
            {" "} / {" "}
            <div className="earnings">
              Winning
              {" "}
              <span>${amount || amount.toFixed(2)}</span>
            </div>
          </div>
        </div>
        <section className={moneyLineClass}>
          <div className="live-moneyline__pmr-line">
            <div
              className="live-moneyline__current-position"
              style={{ left: `${percent}%` }}
            ></div>
            <div className="live-moneyline__winners" style={{ width: `${contest.percentageCanWin}%` }}></div>
          </div>
        </section>
        <div className="menu">
          <div className={`title${(this.state.currentTab === STANDINGS_TAB ? ' active' : '')}`}
            onClick={this.handleViewStandings}
          >
            Standings
            <div className="border"></div>
          </div>
          <div className={`title${(this.state.currentTab === OWNERSHIP_TAB ? ' active' : '')}`}
            onClick={this.handleViewOwnership}
          >
            Players
            <div className="border"></div>
          </div>
        </div>
      </div>
    );
  },

  renderSearchForm() {
    return (
      <div className={`search${(this.state.search ? ' active' : '')}`}>
        <div className="icon" onClick={this.handleFocusSearch}></div>
        <input type="text"
          ref="search"
          value={this.state.searchValue}
          placeholder={this.state.searchPlaceholder}
          onChange={this.handleSearchTermChanged}
        />
      </div>
    );
  },

  renderPages() {
    const { page } = this.state;
    const maxPage = this.getMaxPage();

    const pages = (new Array(maxPage)).join(',').split(',').map((a, i) =>
      <div key={i} className={`page${((page - 1) === i ? ' selected' : '')}`}></div>
    );

    // if only one page, then don't show paginator
    if (maxPage <= 1) {
      return null;
    }

    return (
      <div className="live-standings-pane__pages">
        <div
          className="arrow-left"
          onClick={this.handleViewPrevPage}
        >
          <span>&lt;</span>
        </div>
        {pages}
        <div
          className="arrow-right"
          onClick={this.handleViewNextPage}
        >
          <span>&gt;</span>
        </div>
      </div>
    );
  },

  renderStandings() {
    const lineupsUsernames = this.props.contest.lineupsUsernames;
    const { page, perPage } = this.state;
    let data = this.getListData();
    data = data.slice(
      (page - 1) * perPage,
      Math.min(page * perPage, data.length)
    );
    const watching = this.props.watching;

    const standings = data.filter((lineup) => lineup.id !== 1).map((lineup) => {
      const decimalRemaining = lineup.timeRemaining.decimal;
      let className = 'lineup';
      let pmr = (
        <LivePMRProgressBar
          decimalRemaining={decimalRemaining}
          strokeWidth={2}
          backgroundHex="46495e"
          hexStart="ffffff"
          hexEnd="ffffff"
          svgWidth={50}
          id={`${lineup.id}Lineup`}
        />
      );
      let overlay = (
        <div
          className="overlay"
          onClick={this.handleViewOpponentLineup.bind(this, lineup.id)}
        >
          Watch Live Matchup
        </div>
      );

      if (watching.myLineupId === lineup.id) {
        overlay = '';
        className += ' lineup--mine';
        pmr = (
          <LivePMRProgressBar
            decimalRemaining={decimalRemaining}
            strokeWidth={2}
            backgroundHex="46495e"
            hexStart="34B4CC"
            hexEnd="2871AC"
            svgWidth={50}
            id={`${lineup.id}Lineup`}
          />
        );
      }
      const username = lineupsUsernames[lineup.id] || '';
      let earningsClass = 'lineup--score-earnings';
      let potentialWinnings = lineup.potentialWinnings;
      if (potentialWinnings !== 0) {
        earningsClass += ' in-the-money';
        potentialWinnings = potentialWinnings.toFixed(2);
      }
      return (
        <div key={lineup.id} className={ className }>
          <div className="lineup--place">{lineup.rank}</div>
          { pmr }
          <div className="lineup--score-name">{username}</div>
          <div className="lineup--score-points">{humanizeFP(lineup.fp)} Pts</div>
          <div className={earningsClass}>${potentialWinnings}</div>
          { overlay }
        </div>
      );
    });

    let headers = null;
    if (standings.length) {
      headers = (
        <div className="header">
          <div className="pmr">PMR</div>
          <div className="pts">PTS</div>
          <div className="prize">Prize</div>
        </div>
      );
    }

    return (
      <div className="standings-list">
        {headers}
        {standings}
      </div>
    );
  },

  renderPlayers() {
    const { page, perPage } = this.state;
    let data = this.getListData();
    data = data.slice(
      (page - 1) * perPage,
      Math.min(page * perPage, data.length)
    );

    const players = data.map((player) => {
      const isWatched = this.state.playersWatched.indexOf(player.id) !== -1;
      const overlayTitle = isWatched ? 'Remove from watch' : 'Add to watch';
      const progressHexStart = isWatched ? '422752' : 'ffffff';
      const progressHexEnd = isWatched ? 'ff0000' : 'ffffff';

      return (
        <div key={player.id} className={`player ${isWatched ? 'watched' : ''}`}>
          <div className="player--position">{player.position}</div>
          <div className="player--pmr-photo">
            <LivePMRProgressBar
              decimalRemaining={player.timeRemaining.decimal}
              strokeWidth={3}
              backgroundHex="46495e"
              hexStart={progressHexStart}
              hexEnd={progressHexEnd}
              svgWidth={50}
              id={`${player.id}StandingsPlayer`}
            />
            <div className="avatar" />
          </div>
          <div className="player--name">
            {player.name} <div className="team">{player.team_alias}</div>
          </div>
          <div className="player--points"><b>{humanizeFP(player.fp)}</b><span>Pts</span></div>
          <div className="player--progress">{player.ownershipPercent}%</div>
          <div
            className="player--overlay"
            onClick={this.handleToggleWatchPlayer.bind(this, player.id)}
          >
            {overlayTitle}
          </div>
        </div>
      );
    });

    let pmrClass = '';
    let ptsClass = '';
    let ownedClass = '';
    let sorterClass = ' sorter';

    if (this.state.playersSortAsc) {
      sorterClass += ' asc';
    } else {
      sorterClass += ' desc';
    }

    if (this.state.playersSortKey === 'pmr') {
      pmrClass = sorterClass;
    } else if (this.state.playersSortKey === 'pts') {
      ptsClass = sorterClass;
    } else if (this.state.playersSortKey === 'owned') {
      ownedClass = sorterClass;
    }

    let headers = null;
    if (players.length) {
      let icon = (
        <svg
          className="icon icon-arrow down-arrow-icon"
          height="7"
          onClick={this.handleScrollRight}
          viewBox="0 0 16 16"
          width="7"
        >
          <g>
            <line strokeWidth="2.5" x1="10.3" y1="2.3" x2="4.5" y2="8.1" />
            <line strokeWidth="2.5" x1="3.6" y1="7.3" x2="10.1" y2="13.8" />
          </g>
        </svg>
      );

      headers = (
        <div className="header">
          <div className={`pmr ${pmrClass}`}>
            <span onClick={this.handleSortPlayers.bind(this, 'pmr')}>
              {icon} PMR
            </span>
          </div>
          <div className={`pts ${ptsClass}`}>
            <span onClick={this.handleSortPlayers.bind(this, 'pts')}>
              {icon} PTS
            </span>
          </div>
          <div className={`owned ${ownedClass}`}>
            <span onClick={this.handleSortPlayers.bind(this, 'owned')}>
              {icon} {" "} % Owned
            </span>
          </div>
        </div>
      );
    }

    return (
      <div className="ownership-list">
        {headers}
        {players}
      </div>
    );
  },

  renderStandingsTab() {
    if (this.state.currentTab !== STANDINGS_TAB) return null;

    // wait for usernames
    if (this.props.contest.hasLineupsUsernames === false) return null;

    return (
      <div className="inner">
        {this.renderHeader()}
        {this.renderSearchForm()}
        {this.renderStandings()}
        {this.renderPages()}
      </div>
    );
  },

  renderOwnershipTab() {
    if (this.state.currentTab !== OWNERSHIP_TAB) return null;
    const watchVillain = this.props.watching.villainLineup ? (
      <div className="watch-live" onClick={this.handleWatchVillainLineup}>
        Watch villain lineup
      </div>
    ) : null;

    return (
      <div className="inner">
        {this.renderHeader()}
        {watchVillain}
        {this.renderSearchForm()}
        {this.renderPlayers()}
        {this.renderPages()}
      </div>
    );
  },

  render() {
    const classNames = `live-pane live-pane--right live-standings-pane live-standings-pane--${this.state.currentTab}`;

    return (
      <div className={classNames}>
        <div className="live-pane__back" onClick={this.backToContestsPane}></div>
        {this.renderStandingsTab()}
        {this.renderOwnershipTab()}
      </div>
    );
  },
});

// Redux integration
const { connect } = ReactRedux;

// Wrap the component to inject dispatch and selected state into it.
export default connect(
  () => ({}),
  mapDispatchToProps
)(LiveStandingsPane);
