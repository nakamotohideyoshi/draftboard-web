import React from 'react';
import ImageLoader from 'react-imageloader';
import * as ReactRedux from 'react-redux';
import moment from 'moment';
import store from '../../store';
import * as AppActions from '../../stores/app-state-store.js';
import renderComponent from '../../lib/render-component';
import { forEach as _forEach } from 'lodash';
import { focusedPlayerSelector } from '../../selectors/draft-selectors.js';
import { roundUpToDecimalPlace } from '../../lib/utils.js';
import { createLineupAddPlayer, removePlayer } from '../../actions/lineup-actions.js';

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
  };
}


/**
 * The player detail slideout panel on the draft page. This will display the player info for
 * whatever the DraftGroupActivePlayerStore.activePlayer is.
 */
const DraftPlayerDetail = React.createClass({

  propTypes: {
    player: React.PropTypes.object,
    draftPlayer: React.PropTypes.func,
    unDraftPlayer: React.PropTypes.func,
  },


  getInitialState() {
    return {
      activeTab: 'reports',
    };
  },


  onDraftClick(player, e) {
    e.stopPropagation();
    this.props.draftPlayer(player);
  },


  onUnDraftClick(player, e) {
    e.stopPropagation();
    this.props.unDraftPlayer(player.player_id);
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

    if (!Object.keys(this.props.player.boxScoreHistory).length) {
      content.push(
        <li colSpan="10">Loading...</li>
      );
    }


    switch (this.props.player.sport) {
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
              <td>MIN</td>
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

    if (!Object.keys(this.props.player.news).length) {
      news = (
        <div><h5>No recent news updates.</h5></div>
      );
    }

    _forEach(this.props.player.news, (item) => {
      news.push(
        <article key={item.tsxitem.srid} className="report">
          <header className="header">
            <address className="byline">{item.tsxitem.credit}</address>
            <h5 className="title">{item.tsxitem.title}</h5>
          </header>
          <section className="content">
            <p>{item.tsxitem.content}</p>
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


  renderStatsAverage() {
    const player = this.props.player;

    if (!Object.keys(player.boxScoreHistory).length) {
      return <div className="player-stats"></div>;
    }


    switch (player.sport) {
      case 'nba':
        return (
          <div className="player-stats">
            <ul>
              <li>
                <div className="stat-name">PPG</div>
                <div className="stat-score">
                  {roundUpToDecimalPlace(player.boxScoreHistory.avg_points, 1)}
                </div>
              </li>
              <li>
                <div className="stat-name">RPG</div>
                <div className="stat-score">
                  {roundUpToDecimalPlace(player.boxScoreHistory.avg_rebounds, 1)}
                </div>
              </li>
              <li>
                <div className="stat-name">APG</div>
                <div className="stat-score">
                  {roundUpToDecimalPlace(player.boxScoreHistory.avg_assists, 1)}
                </div>
              </li>
              <li>
                <div className="stat-name">STLPG</div>
                <div className="stat-score">
                  {roundUpToDecimalPlace(player.boxScoreHistory.avg_steals, 1)}
                </div>
              </li>
              <li>
                <div className="stat-name">TO</div>
                <div className="stat-score">
                  {roundUpToDecimalPlace(player.boxScoreHistory.avg_turnovers, 1)}
                </div>
              </li>
              <li>
                <div className="stat-name">FPPG</div>
                <div className="stat-score">
                  {roundUpToDecimalPlace(player.fppg, 1)}
                </div>
              </li>
            </ul>
          </div>
        );

      case 'nhl':
      // For NHL goalies:
        if (player.position === 'G') {
          return (
            <div className="player-stats">
              <ul>
                <li>
                  <div className="stat-name">S</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(player.boxScoreHistory.avg_saves, 1)}
                  </div>
                </li>
                <li>
                  <div className="stat-name">A</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(player.boxScoreHistory.avg_assist, 1)}
                  </div>
                </li>
                <li>
                  <div className="stat-name">SOG</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(player.boxScoreHistory.avg_sog, 1)}
                  </div>
                </li>
                <li>
                  <div className="stat-name">FPPG</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(player.boxScoreHistory.avg_fp, 1)}
                  </div>
                </li>
              </ul>
            </div>
          );
        }
        // For regular NHL Players:
        return (
          <div className="player-stats">
            <ul>
              <li>
                <div className="stat-name">G</div>
                <div className="stat-score">
                  {roundUpToDecimalPlace(player.boxScoreHistory.avg_goal, 1)}
                </div>
              </li>
              <li>
                <div className="stat-name">A</div>
                <div className="stat-score">
                  {roundUpToDecimalPlace(player.boxScoreHistory.avg_assist, 1)}
                </div>
              </li>
              <li>
                <div className="stat-name">BLK</div>
                <div className="stat-score">
                  {roundUpToDecimalPlace(player.boxScoreHistory.avg_blk, 1)}
                </div>
              </li>
              <li>
                <div className="stat-name">SOG</div>
                <div className="stat-score">
                  {roundUpToDecimalPlace(player.boxScoreHistory.avg_sog, 1)}
                </div>
              </li>
              <li>
                <div className="stat-name">FPPG</div>
                <div className="stat-score">
                  {roundUpToDecimalPlace(player.boxScoreHistory.avg_fp, 1)}
                </div>
              </li>
            </ul>
          </div>
        );

      default:
        return <div className="player-stats"></div>;
    }
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

    return (
      <div className="draft-player-detail player-detail-pane">
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

          { this.renderStatsAverage() }
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
