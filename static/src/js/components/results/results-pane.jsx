import React from 'react';
import renderComponent from '../../lib/render-component';
import store from '../../store';
import PrizeStructure from '../contest-list/prize-structure.jsx';
import GamesList from '../contest-list/games-list.jsx';
// import EntrantList from '../contest-list/entrant-list.jsx';
import { fetchContestIfNeeded } from '../../actions/live-contests';
import { fetchContestLineupsUsernamesIfNeeded } from '../../actions/live-contests';
import { fetchDraftGroupBoxscoresIfNeeded } from '../../actions/live-draft-groups.js';
import { resultsContestsSelector } from '../../selectors/results-contests';
import { Provider, connect } from 'react-redux';


const ResultsPane = React.createClass({

  propTypes: {
    contestId: React.PropTypes.number,
    dispatch: React.PropTypes.func.isRequired,
    entry: React.PropTypes.object.isRequired,
    resultsContestsSelector: React.PropTypes.object.isRequired,
    onHide: React.PropTypes.func,
    numToPlace: React.PropTypes.func,
  },

  getInitialState() {
    return {
      activeTab: 'standings',
    };
  },

  componentWillMount() {
    document.body.classList.add('results-pane');
  },

  componentWillUpdate(nextProps) {
    if (nextProps.contestId !== null && nextProps.contestId !== this.props.contestId) {
      this.props.dispatch(
        fetchContestIfNeeded(nextProps.contestId, true)
      ).then(() => {
        const newContestInfo = this.props.resultsContestsSelector[this.props.contestId];

        this.props.dispatch(fetchContestLineupsUsernamesIfNeeded(this.props.contestId));
        this.props.dispatch(fetchDraftGroupBoxscoresIfNeeded(newContestInfo.draftGroupId));
      });
    }
  },

  componentWillUnmount() {
    document.body.classList.remove('results-pane');
  },

  // I know making these their own components would be more 'react', but I don't want to deal with
  // the hassle right now.
  getTabNav() {
    const tabs = [
      { title: 'Payout', tab: 'prizes' },
      { title: 'Games', tab: 'games' },
      { title: 'Scoring', tab: 'scoring' },
      { title: 'Standings', tab: 'standings' },
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

  renderStandings(contest) {
    const standings = contest.rankedLineups.map((lineupId) => {
      const lineup = contest.lineups[lineupId];
      const username = (lineup.user) ? lineup.user.username : `user${lineupId}`;

      return (
        <tr key={lineup.id}>
          <td>{username}</td>
          <td>${lineup.potentialEarnings.toFixed(2)}</td>
        </tr>
      );
    });

    return (
      <table className="table">
        <thead>
          <tr>
            <th>entry</th>
            <th>prize</th>
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
    const contest = this.props.resultsContestsSelector[this.props.contestId] || {};

    switch (this.state.activeTab) {
      case 'prizes':
        return (<PrizeStructure structure={contest.prizeStructure} />);

      case 'games':
        if (contest.boxScores !== null) {
          return (
            <GamesList
              boxScores={contest.boxScores}
              teams={contest.teams}
            />
          );
        }

        return 'No boxscore info available.';

      case 'scoring':
        return 'No scoring info available.';

      case 'standings':
        return this.renderStandings(contest);

      default:
        return ('Select a tab');
    }
  },

  render() {
    const contest = this.props.resultsContestsSelector[this.props.contestId] || {};
    const entry = this.props.entry;
    const tabNav = this.getTabNav();

    // show loading until we have data
    if (contest.hasOwnProperty('prizeStructure') === false || contest.boxScores === null) {
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

    const prize = contest.prizeStructure.info.ranks[0].value.toFixed(2);

    return (
      <section className="pane pane--contest-detail pane--contest-results">
        <div className="pane__close" onClick={this.handleHide}></div>

        <div className="pane__content">
          <div className="pane-upper">
            <div className="header">
              <div className="has-ended">
                This contest has ended
              </div>
              <div className="header__content">
                <div className="title">
                  {contest.name}<br />
                (${prize} to 1st)
              </div>
              <div className="header__info">
                <div className="header__place">
                  <div className="info-title">place</div>
                  <span>{this.props.numToPlace(entry.final_rank)}</span>
                </div>
              </div>

              <div className="header__extra-info">
                <div className="m badge">M</div>
                <div className="g badge">G</div>
              </div>

              <div className="header__fee-prizes-pool">
                <div><span className="info-title">Prize</span><div>${prize}</div></div>
                <div><span className="info-title">Fee</span><div>${contest.buyin.toFixed(2)}</div></div>
                <div><span className="info-title">Entrants</span><div>
                  {contest.rankedLineups.length}/{contest.entriesCount}
                </div></div>
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
  resultsContestsSelector: resultsContestsSelector(state),
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
