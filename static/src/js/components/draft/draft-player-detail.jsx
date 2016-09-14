import React from 'react';
import PubSub from 'pubsub-js';
import ImageLoader from 'react-imageloader';
import * as ReactRedux from 'react-redux';
import moment from 'moment';
import store from '../../store';
import * as AppActions from '../../stores/app-state-store';
import renderComponent from '../../lib/render-component';
import forEach from 'lodash/forEach';
import { focusedPlayerSelector } from '../../selectors/draft-selectors';
import { createLineupAddPlayer, removePlayer } from '../../actions/upcoming-lineup-actions';
import { focusPlayerSearchField, clearPlayerSearchField } from './draft-utils';
import { fetchSinglePlayerBoxScoreHistoryIfNeeded } from '../../actions/player-box-score-history-actions';
import DraftPlayerDetailAverages from './draft-player-detail-averages';

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
      this.props.fetchSinglePlayerBoxScoreHistoryIfNeeded(
        nextProps.player.sport, nextProps.player.player_id
      );
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
          {tab.title}
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
    const content = [];
    let headers = [];

    if (!this.props.player.splitsHistory) {
      content.push(
        <tr key="header"><td colSpan="10"><h5>Loading...</h5></td></tr>
      );
    }


    switch (this.props.player.sport) {
      case 'nfl':
        headers = [
          <th key="opp">opp</th>,
          <th key="date">date</th>,
          <th key="py">pass yds</th>,
          <th key="pt">pass td</th>,
          <th key="pi">pass int</th>,
          <th key="ry">rush yds</th>,
          <th key="rt">rush td</th>,
          <th key="rcy">rec yds</th>,
          <th key="rct">rec td</th>,
          <th key="fum">fum</th>,
          <th key="fp">fp</th>,
        ];

        this.props.player.splitsHistory.map((game, index) => {
          content.push(
            <tr key={index}>
              <td key="1">{game.opp}</td>
              <td key="2">{moment.utc(game.date).format('M/D/YY')}</td>
              <td key="3">{game.pass_yds}</td>
              <td key="4">{game.pass_td}</td>
              <td key="5">{game.pass_int}</td>
              <td key="6">{game.rush_yds}</td>
              <td key="7">{game.rush_td}</td>
              <td key="8">{game.rec_yds}</td>
              <td key="9">{game.rec_td}</td>
              <td key="10">{game.off_fum_lost}</td>
              <td key="11">{game.fp}</td>
            </tr>
          );
        });

        break;

      case 'nba':
        headers = [
          <th>opp</th>,
          <th>date</th>,
          <th>pts</th>,
          <th>reb</th>,
          <th>ast</th>,
          <th>blk</th>,
          <th>stl</th>,
          <th>min</th>,
          <th>to</th>,
          <th>fp</th>,
        ];

        this.props.player.splitsHistory.map((game, index) => {
          content.push(
            <tr key={index}>
              <td>{game.opp}</td>

              <td>{moment(game.date, moment.ISO_8601).format('M/D/YY')}</td>
              <td>{game.points}</td>
              <td>{game.rebounds}</td>
              <td>{game.assists}</td>
              <td>{game.blocks}</td>
              <td>{game.steals}</td>
              <td>{game.minutes}</td>
              <td>{game.turnovers}</td>
              <td>{game.fp}</td>
            </tr>
          );
        });

        break;
      case 'nhl':
        headers = [
          <th>opp</th>,
          <th>date</th>,
          <th>g</th>,
          <th>ast</th>,
          <th>blk</th>,
          <th>sog</th>,
          <th>s</th>,
          <th>ga</th>,
          <th>fp</th>,
        ];

        this.props.player.splitsHistory.map((game, index) => {
          content.push(
            <tr key={index}>
              <td>{game.opp}</td>
              <td>{moment(game.date, moment.ISO_8601).format('M/D/YY')}</td>
              <td>{game.goal}</td>
              <td>{game.assist}</td>
              <td>{game.blocks}</td>
              <td>{game.sog}</td>
              <td>{game.saves}</td>
              <td>{game.ga}</td>
              <td>{game.fp}</td>
            </tr>
          );
        });

        break;
      default:
        // show nothing.
    }


    return (
      <div className="player-splits">
        <table className="table">
          <thead className="header">
            <tr>
              {headers}
            </tr>
          </thead>
          <tbody>
            {content}
          </tbody>
        </table>
      </div>
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
      news.push(
        <article key={i} className="report">
          <header className="header">
            <address className="byline">
              <a rel="nofollow" target="_blank" href={item.url_origin}>{item.source_origin}</a>&nbsp;
              <span className="timestamp">{moment.utc(item.updated_at).fromNow()}</span>
            </address>

            <h5 className="title">{item.status}</h5>
          </header>
          <section className="content">
            <p>{item.value}</p>
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
            <ul className="tab-nav">{tabNav}</ul>

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
