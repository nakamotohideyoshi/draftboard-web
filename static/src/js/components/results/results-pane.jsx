import PrizeStructure from '../contest-list/prize-structure.jsx';
import React from 'react';
import renderComponent from '../../lib/render-component';
import store from '../../store';
import { humanizeCurrency } from '../../lib/utils/currency';
import { addOrdinal } from '../../lib/utils/numbers';
import { Provider, connect } from 'react-redux';
import { focusedContestResultSelector } from '../../selectors/results-contests';
import ScoringInfo from '../contest-list/scoring-info';


const ResultsPane = React.createClass({

  propTypes: {
    contestId: React.PropTypes.number,
    dispatch: React.PropTypes.func.isRequired,
    entry: React.PropTypes.object.isRequired,
    onHide: React.PropTypes.func,
    sport: React.PropTypes.string.isRequired,
    contestResult: React.PropTypes.object.isRequired,
  },


  getInitialState() {
    return {
      activeTab: 'standings',
    };
  },


  componentWillMount() {
    document.body.classList.add('results-pane');
  },


  componentWillUnmount() {
    document.body.classList.remove('results-pane');
  },


  // I know making these their own components would be more 'react', but I don't want to deal with
  // the hassle right now.
  getTabNav() {
    const tabs = [
      { title: 'Standings', tab: 'standings' },
      { title: 'Payout', tab: 'prizes' },
      { title: 'Games', tab: 'games' },
      { title: 'Scoring', tab: 'scoring' },
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


  handleHide() {
    this.props.onHide();
  },


  // When a tab is clicked, tell the state to show it'scontent.
  handleTabClick(tabName) {
    this.setState({ activeTab: tabName });
  },


  renderStandings(rankedEntries) {
    const standings = rankedEntries.map((entry) => {
      let lineupPlayers = [];
      if (entry.lineup) {
        lineupPlayers = entry.lineup.players.map((player) => {
          return (<span key={player.idx}>{player.full_name} - {player.fantasy_points} FP</span>);
        });
      }
      let payout = 0.0;

      if (entry.payout) {
        payout = entry.payout.amount;
      }

      return (
        <tr key={entry.username}>
          <td>{entry.username}</td>
          <td>{humanizeCurrency(payout)}</td>
          <td>{entry.fantasy_points}</td>
          <td>
            <h4>Players</h4>
            {lineupPlayers}
          </td>
        </tr>
      );
    });

    return (
      <table className="table">
        <thead>
          <tr>
            <th>entry</th>
            <th>prize</th>
            <th>points</th>
          </tr>
        </thead>
        <tbody>
          {standings}
        </tbody>
      </table>
    );
  },


  // Get the content of the selected tab.
  renderActiveTab() {
    const contest = this.props.contestResult || {};

    switch (this.state.activeTab) {
      case 'prizes': {
        return (<PrizeStructure structure={this.props.contestResult.prize_structure} />);
      }

      case 'games': {
        const gameList = this.props.contestResult.games.map((game) => (
            <tr key={game.home_team}>
              <td className="teams">
                {game.away_team}&nbsp;vs&nbsp;
                {game.home_team}
              </td>
            </tr>
        ));

        if (contest.games !== null) {
          return (
            <div className="cmp-games-list">

              <table className="table">
                <thead>
                  <tr>
                    <th className="place">Teams</th>
                  </tr>
                </thead>
                <tbody>
                  {gameList}
                </tbody>
              </table>
            </div>
          );
        }

        return 'No boxscore info available.';
      }

      case 'scoring': {
        return <ScoringInfo sport={contest.sport} />;
      }

      case 'standings': {
        return this.renderStandings(this.props.contestResult.ranked_entries);
      }

      default: {
        return ('Select a tab');
      }
    }
  },


  render() {
    const contest = this.props.contestResult || {};
    const entry = find(this.props.contestResult, { id: this.props.entry.id });
    const tabNav = this.getTabNav();
    const prizeStructure = this.props.contestResult.prize_structure;

    // show loading until we have data
    if (Object.keys(this.props.contestResult).length === 0) {
      return (
        <section className="pane pane--contest-detail pane--contest-results">
          <div className="pane__close" onClick={this.handleHide}></div>

          <div className="pane__content">
            <div className="pane-upper">
              <div className="header">
                <div className="loading">
                  <div className="preload-court" />
                  <div className="spinner">
                    <div className="double-bounce1" />
                    <div className="double-bounce2" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      );
    }

    const prize = humanizeCurrency(prizeStructure.ranks[0].value);

    let hasEnded = (
      <div className="has-ended">
        This contest has ended
      </div>
    );
    if (entry.hasNotEnded === true) {
      hasEnded = (<div />);
    }

    return (
      <section className="pane pane--contest-detail pane--contest-results">
        <div className="pane__close" onClick={this.handleHide}></div>

        <div className="pane__content">
          <div className="pane-upper">
            <div className="header">
              {hasEnded}
              <div className="header__content">
                <div className="title">
                  {contest.name}<br />
                ({prize} to 1st)
              </div>
              <div className="header__info">
                <div className="header__place">
                  <div className="info-title">place</div>
                  <span>{addOrdinal(entry.final_rank)}</span>
                </div>
              </div>

              <div className="header__fee-prizes-pool">
                <div><span className="info-title">Prize Pool</span><div>{humanizeCurrency(prize)}</div></div>
                <div><span className="info-title">Entries</span><div>
                  {contest.current_entries}/{contest.entries}
                </div></div>
                <div><span className="info-title">PLACE / WON</span><div>{humanizeCurrency(contest.buyin)}</div></div>
              </div>
            </div>
          </div>
          </div>

          <div colSpan="9" className="pane-lower">
            <ul className="tab-nav">{tabNav}</ul>
            <div className="tab-content">{this.renderActiveTab()}</div>
          </div>

        </div>
      </section>
    );
  },
});


// Which part of the Redux global state does our component want to receive as props?
const mapStateToProps = (state) => ({
  contestResult: focusedContestResultSelector(state),
});

// Wrap the component to inject dispatch and selected state into it.
const ResultsPaneConnected = connect(
  mapStateToProps
)(ResultsPane);


renderComponent(
  <Provider store={store}>
    <ResultsPaneConnected />
  </Provider>
);

export default ResultsPaneConnected;
