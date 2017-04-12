import React from 'react';
import PubSub from 'pubsub-js';
import ImageLoader from 'react-imageloader';
import * as ReactRedux from 'react-redux';
import moment from 'moment';
import store from '../../store';
import * as AppActions from '../../stores/app-state-store';
import renderComponent from '../../lib/render-component';
import forEach from 'lodash/forEach';
import get from 'lodash/get';
import { focusedPlayerSelector } from '../../selectors/draft-selectors';
import { createLineupAddPlayer, removePlayer } from '../../actions/upcoming-lineup-actions';
import { focusPlayerSearchField, clearPlayerSearchField } from './draft-utils';
import { fetchSinglePlayerBoxScoreHistoryIfNeeded,
fetchSinglePlayerNews } from '../../actions/player-box-score-history-actions';
import DraftPlayerDetailAverages from './draft-player-detail-averages';
import DraftPlayerDetailGameLogs from './draft-player-detail-game-logs';

const { Provider, connect } = ReactRedux;

/**
 * What shows when a player image is loading
 * @return {JSX}
 */
function preloader() {
  return (
    <div className="loading-player-image">
      <div className="spinner">
        <div className="double-bounce1" />
        <div className="double-bounce2" />
      </div>
    </div>
  );
}

/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
function mapStateToProps(state) {
  return {
    player: focusedPlayerSelector(state),
  };
}

/*
 * Map Redux actions to React component properties
 * @param  {function} dispatch The dispatch method to pass actions into
 * @return {object}            All of the methods to map to the component
 */
function mapDispatchToProps(dispatch) {
  return {
    draftPlayer: (player) => dispatch(createLineupAddPlayer(player)),
    unDraftPlayer: (playerId) => dispatch(removePlayer(playerId)),
    fetchSinglePlayerBoxScoreHistoryIfNeeded: (sport, playerId) =>
      dispatch(fetchSinglePlayerBoxScoreHistoryIfNeeded(sport, playerId)),
    fetchSinglePlayerNews: (sport, playerSrid) => dispatch(fetchSinglePlayerNews(sport, playerSrid)),
  };
}


/**
 * The player detail slideout panel on the draft page. This will display the player info for
 * whatever the DraftGroupActivePlayerStore.activePlayer is.
 */
const DraftPlayerDetail = React.createClass({

  propTypes: {
    player: React.PropTypes.object,
    draftPlayer: React.PropTypes.func.isRequired,
    unDraftPlayer: React.PropTypes.func.isRequired,
    fetchSinglePlayerBoxScoreHistoryIfNeeded: React.PropTypes.func.isRequired,
    fetchSinglePlayerNews: React.PropTypes.func.isRequired,
  },


  getInitialState() {
    return {
      activeTab: 'reports',
    };
  },


  componentWillMount() {
    PubSub.subscribe('pane.close', () => {
      focusPlayerSearchField();
    });
  },


  componentWillReceiveProps(nextProps) {
    // If we have a valid player id, fetch the boxscore history. The action + reducer layers will
    // take care of any caching needs for us.
    if (nextProps.player && 'player_id' in nextProps.player) {
      if (get(this.props, 'player.player_id') !== get(nextProps, 'player.player_id')) {
        this.props.fetchSinglePlayerBoxScoreHistoryIfNeeded(
          nextProps.player.sport, nextProps.player.player_id
        );
        this.props.fetchSinglePlayerNews(
          nextProps.player.sport, nextProps.player.player_srid
        );
      }
    }
  },


  onDraftClick(player, e) {
    e.stopPropagation();
    this.props.draftPlayer(player);
    clearPlayerSearchField();
  },


  onUnDraftClick(player, e) {
    e.stopPropagation();
    this.props.unDraftPlayer(player.player_id);
    clearPlayerSearchField();
  },


  getActiveTabContent() {
    switch (this.state.activeTab) {
      case 'reports':
        return this.renderPlayerNews();
      case 'splits':
        return this.renderPlayerSplits();
      default:
        return this.renderPlayerNews();
    }
  },


  /**
   * Build the player detail panel.
   */
  getPlayerDetail() {
    if (this.props.player) {
      return (
        <div className="player-detail-pane">
          <div className="cmp-draft-player-detail__player-inner">
            <h6 className="cmp-draft-player-detail__team">
              {this.props.player.team_alias} - {this.props.player.position}
            </h6>

            <h2 className="cmp-draft-player-detail__name">
              {this.props.player.name}
            </h2>
          </div>

          <div className="cmp-draft-player-detail__salary">
            <h3>${this.props.player.salary.toLocaleString('en')}</h3>
          </div>

        </div>
      );
    }

    return ('');
  },


  getDraftButton() {
    // the player is drafted - show remove button.
    if (this.props.player.drafted) {
      return (
        <div
          className="draft-button remove"
          onClick={this.onUnDraftClick.bind(this, this.props.player)}
        >Remove</div>
      );
    }

    // the player is not eligible to draft - show disabled button.
    if (!this.props.player.draftable) {
      return (
        <div className="draft-button disabled">Draft</div>
      );
    }

    // the player is draftable - show draft button.
    return (
      <div
        className="draft-button"
        onClick={this.onDraftClick.bind(this, this.props.player)}
      >Draft</div>
    );
  },


  // I know making these their own components would be more 'react', but I don't want to deal with
  // the hassle right now.
  getTabNav() {
    const tabs = [
      { title: 'Updates', tab: 'reports' },
      { title: 'Game Log', tab: 'splits' },
    ];

    return tabs.map((tab) => {
      let classes = '';

      if (this.state.activeTab === tab.tab) {
        classes = 'active';
      }

      return (
        <li
          key={tab.tab}
          className={classes}
          onClick={this.handleTabClick.bind(this, tab.tab)}
        >
          <span className="tab-title">
            {tab.title}
          </span>
        </li>
      );
    });
  },


  close() {
    AppActions.closePane();
  },


  // When a tab is clicked, tell the state to show it'scontent.
  handleTabClick(tabName) {
    this.setState({ activeTab: tabName });
  },


  renderPlayerSplits() {
    return (
      <DraftPlayerDetailGameLogs player={this.props.player} />
    );
  },


  renderNextGameInfo() {
    if (!this.props.player.nextGame || !Object.keys(this.props.player.nextGame).length) {
      return (
        <div className="next-game">Loading...</div>
      );
    }

    return (
      <div className="next-game">
        <h4 className="team away-team">
          <span
            className={
              `city ${this.props.player.sport}-${this.props.player.nextGame.awayTeam.alias.toLowerCase()}-2-text`
            }
          >
            {this.props.player.nextGame.awayTeam.city}
          </span>
          <span
            className={
              `name ${this.props.player.sport}-${this.props.player.nextGame.awayTeam.alias.toLowerCase()}-1-text`
            }
          >
            {this.props.player.nextGame.awayTeam.name}
          </span>
        </h4>

        <div className="game-time"><span className="time">
          {moment(this.props.player.nextGame.start).format('h:mma')}
        </span></div>

        <h4 className="team home-team">
          <span className={
              `city ${this.props.player.sport}-${this.props.player.nextGame.homeTeam.alias.toLowerCase()}-2-text`
            }
          >
            {this.props.player.nextGame.homeTeam.city}
          </span>
          <span className={
              `name ${this.props.player.sport}-${this.props.player.nextGame.homeTeam.alias.toLowerCase()}-1-text`
            }
          >
            {this.props.player.nextGame.homeTeam.name}
          </span>
        </h4>
      </div>
    );
  },


  renderPlayerNews() {
    let news = [];
    if (!this.props.player.news) {
      news = (
        <div><h5>No recent news updates.</h5></div>
      );
    }

    forEach(this.props.player.news, (item, i) => {
    // <a rel="nofollow" target="_blank" href={item.url_origin}>{item.source_origin}</a>&nbsp;
      news.push(
        <article key={i} className="report">
          <header className="header">
            <address className="byline">
              <span className="timestamp">{moment.utc(item.updated_at).fromNow()}</span>
            </address>
            <h5 className="title">{item.headline}</h5>
          </header>
          <section className="content">
            <p>{item.notes}</p>
          </section>
          <header className="header">
            <h5 className="title">Analysis</h5>
          </header>
          <section className="content">
            <p>{item.analysis}</p>
          </section>
        </article>
      );
    });

    return (
      <div className="player-reports">
        {news}
      </div>
    );
  },


  render() {
    // No player has been selected.
    if (!this.props.player) {
      return (
        <div className="draft-player-detail player-detail-pane">
          <div className="player-pane-inner">Select a Player</div>
        </div>
      );
    }

    const player = this.props.player;
    const tabNav = this.getTabNav();
    const playerImagesBaseUrl = `${window.dfs.playerImagesBaseUrl}/${this.props.player.sport}`;
    const paneClass = `draft-player-detail player-detail-pane sport-${this.props.player.sport}`;

    return (
      <div className={paneClass}>
        <div
          onClick={this.close}
          className="pane__close"
        ></div>
        <div className="pane-upper">
          <div className="header-section">
            <div className="header__player-image">
              <ImageLoader
                src={`${playerImagesBaseUrl}/380/${this.props.player.player_srid}.png`}
                wrapper={React.DOM.div}
                preloader={preloader}
              />
            </div>

            <div className="header__team-role">
              {player.teamCity} {player.teamName} - {player.position}
            </div>
            <div className="header__name">{ player.name }</div>

            <div className="draft-salary">
              <div className="draft-status">
                {this.getDraftButton()}
              </div>
              <h3 className="salary">${this.props.player.salary.toLocaleString('en')}</h3>
            </div>
          </div>

          <DraftPlayerDetailAverages player={this.props.player} />
        </div>

        <div className="pane-lower">

          {this.renderNextGameInfo()}

          <section className="tabs">
            <ul className="tab-nav">
              {tabNav}
              <li>
                <a rel="nofollow" target="_blank" href="http://www.rotowire.com/">Updates provided by </a>
                <div className="rotowire-icon"></div>
              </li>
            </ul>

            <div className="tab-content">
              {this.getActiveTabContent()}
            </div>
          </section>
        </div>

      </div>
    );
  },

});


// Wrap the component to inject dispatch and selected state into it.
const DraftPlayerDetailConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(DraftPlayerDetail);

// Render the component.
renderComponent(
  <Provider store={store}>
    <DraftPlayerDetailConnected />
  </Provider>,
  '.cmp-draft-player-detail'
);


module.exports = DraftPlayerDetail;
