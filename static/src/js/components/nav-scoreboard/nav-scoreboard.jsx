import NavScoreboardStatic from './nav-scoreboard-static';
import PusherData from '../site/pusher-data';
import React from 'react';
import renderComponent from '../../lib/render-component';
import store from '../../store';
import { bindActionCreators } from 'redux';
import { fetchCurrentLineupsAndRelated } from '../../actions/current-lineups';
import { fetchSportsIfNeeded } from '../../actions/sports';
import { humanizeCurrency } from '../../lib/utils/currency';
import { myCurrentLineupsSelector } from '../../selectors/current-lineups';
import { Provider, connect } from 'react-redux';
import { removeUnusedContests } from '../../actions/live-contests';
import { removeUnusedDraftGroups } from '../../actions/live-draft-groups';
import { sportsSelector } from '../../selectors/sports';


/*
 * Map Redux actions to React component properties
 * @param  {function} dispatch The dispatch method to pass actions into
 * @return {object}            All of the methods to map to the component, wrapped in 'action' key
 */
const mapDispatchToProps = (dispatch) => ({
  actions: bindActionCreators({
    fetchCurrentLineupsAndRelated,
    fetchSportsIfNeeded,
    removeUnusedContests,
    removeUnusedDraftGroups,
  }, dispatch),
});

/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
const mapStateToProps = (state) => ({
  myCurrentLineupsSelector: myCurrentLineupsSelector(state),
  sportsSelector: sportsSelector(state),
});

/*
 * The overarching component for the scoreboard spanning the top of the site.
 *
 * Most important thing to glean from this comment is that this component is the
 * one that loads all data for the live and scoreboard redux substores!
 */
const NavScoreboard = React.createClass({

  propTypes: {
    actions: React.PropTypes.object.isRequired,
    cashBalance: React.PropTypes.string,
    myCurrentLineupsSelector: React.PropTypes.object.isRequired,
    sportsSelector: React.PropTypes.object.isRequired,
  },


  getDefaultProps() {
    return {
      cashBalance: humanizeCurrency(window.dfs.user.cashBalance),
    };
  },


  getInitialState() {
    return {
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
    this.props.actions.fetchSportsIfNeeded();

    // if the user is logged in
    if (this.state.user.username !== '' && !this.state.isLivePage) {
      this.props.actions.fetchCurrentLineupsAndRelated();
    }

    this.startListening();
  },

  /**
   * Internal method to start listening to pusher and poll for updates
   */
  startListening() {
    // start parity checks
    window.setInterval(() => this.props.actions.fetchSportsIfNeeded(), 5000);

    // remove expired objects within Redux if you aren't on the results page
    if (window.location.pathname.substring(0, 9) !== '/results/') {
      this.props.actions.removeUnusedContests();
      this.props.actions.removeUnusedDraftGroups();
    }
  },

  /**
   * Render slider contents based on selected filter.
   */
  render() {
    return (
      <div>
        <NavScoreboardStatic
          user={window.dfs.user}
          sportsSelector={this.props.sportsSelector}
          myCurrentLineupsSelector={this.props.myCurrentLineupsSelector}
          cashBalance={this.props.cashBalance}
        />
        <PusherData />
      </div>
    );
  },
});

// Wrap the component to inject dispatch and selected state into it.
const NavScoreboardConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(NavScoreboard);

// Uses the Provider to have redux state
renderComponent(
  <Provider store={store}>
    <NavScoreboardConnected />
  </Provider>,
  '.cmp-nav-scoreboard'
);
