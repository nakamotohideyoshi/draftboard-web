import React from 'react'
import ReactDom  from 'react-dom'
const ReactRedux = require('react-redux')
const store = require('../../store')
const LineupCard = require('../lineup/lineup-card.jsx')
const renderComponent = require('../../lib/render-component')
const smoothScrollTo = require('../../lib/smooth-scroll-to.js')
const LobbyDraftGroupSelectionModal = require('./lobby-draft-group-selection-modal.jsx')
import {fetchUpcomingLineups, lineupFocused} from '../../actions/lineup-actions.js'
import {fetchEntriesIfNeeded} from '../../actions/entries'
import {draftGroupInfoSelector} from '../../selectors/draft-group-info-selector.js'
import {LineupsBySportSelector} from '../../selectors/upcoming-lineups-by-sport.js'
import {UpcomingLineupsInfo} from '../../selectors/upcoming-lineups-info.js'
import '../contest-list/contest-list-sport-filter.jsx'


/**
 * Renders a list of lineup cards. Feed it lineup data and it will render LineupCard components for
 * each lineup.
 */
var LineupCardList = React.createClass({

  propTypes: {
    lineupFocused: React.PropTypes.func,
    fetchUpcomingLineups: React.PropTypes.func.isRequired,
    fetchEntriesIfNeeded: React.PropTypes.func.isRequired,
    lineups: React.PropTypes.array.isRequired,
    lineupsInfo: React.PropTypes.object,
    focusedLineupId: React.PropTypes.number,
    draftGroupInfo: React.PropTypes.object
  },

  getDefaultProps: function() {
    return {
      lineups: []
    }
  },


  /**
   * Smoothly scroll to a lineup card.
   * @param  {int} the id of the lineup to scroll to.
   */
  scrollToCard: function(lineupId) {
    var cardDom = ReactDom.findDOMNode(this.refs['lineup-' + lineupId])

    if (cardDom) {
      var scrollingElement = document.querySelector('.sidebar .sidebar-inner')
      smoothScrollTo(scrollingElement, cardDom.offsetTop - 20, 600)
    }
  },


  /**
   * Set a lineupCard as being 'focused' - this un-collapses and scrolls to it.
   * @param  {int}   lineupId   The ID of the lineup.
   */
  setActiveLineup: function(lineupId) {
    this.props.lineupFocused(lineupId);
  },


  componentWillMount: function() {
    if (window.dfs.user.isAuthenticated === true) {
      this.props.fetchEntriesIfNeeded()
      this.props.fetchUpcomingLineups()
    }
  },


  componentDidUpdate: function(prevProps) {
    // We need to wait until the lineup has been activated before it is scrolled to because if the
    // previously activated lineup is above it in the list, the offset dimensions change when it
    // collapses. This will wait until the DOM has been updated and the old focused lineup has
    // collapsed.
    if (this.props.focusedLineupId !== prevProps.focusedLineupId) {
      this.scrollToCard(this.props.focusedLineupId);
    }
  },


  /**
   * Click handler for a lineupCard
   */
  onCardClick: function(lineup) {
    this.setActiveLineup(lineup.id);
  },


  handleDraftButtonClick: function() {
    this.refs.draftModal.open();
  },


  getLineupCards: function() {
    return this.props.lineups.map(function(lineup) {
      // We'll need a reference to the card in order to get it's DOM element and scroll to it when
      // it gets focused.
      var refName = 'lineup-' + lineup.id;
      let draftGroupInfo = {}

      if (this.props.draftGroupInfo.draftGroups.hasOwnProperty(lineup.draft_group)) {
        draftGroupInfo = this.props.draftGroupInfo.draftGroups[lineup.draft_group]
      }

      let entries
      let fees

      if (this.props.lineupsInfo.hasOwnProperty(lineup.id)) {
        fees = this.props.lineupsInfo[lineup.id].fees
        entries = this.props.lineupsInfo[lineup.id].entries
      }

      return (
        <LineupCard
          key={lineup.id}
          lineup={lineup}
          draftGroupInfo={draftGroupInfo}
          isActive={this.props.focusedLineupId === lineup.id}
          ref={refName}
          onCardClick={this.onCardClick}
          fees={fees}
          entries={entries}
        />
      );
    }, this);

  },


  getCreateLineupAd: function() {
    if (this.props.lineups.length > 0) {
      return (
        <div
          className="cmp-lineup-card cmp-lineup-card--collapsed cmp-lineup-card--create-collapsed"
          onClick={this.handleDraftButtonClick}
        >
          <header className="cmp-lineup-card__header">
            <h3 className="cmp-lineup-card__title">
              Create a Lineup <span className="cmp-lineup-card__plus">+</span>
            </h3>
          </header>
        </div>
      )
    }
    else {
      return (
        <div className="cmp-lineup-card cmp-lineup-card--create cmp-lineup-card--create__nba">
          <header className="cmp-lineup-card__header">
            <h3 className="cmp-lineup-card__title">
              <span className="sub">Get in the Action</span>
              <span>Create a Lineup</span>
            </h3>
          </header>

          <div
            className="button button--medium button--gradient-outline"
            onClick={this.handleDraftButtonClick}
          >
            Draft a Team
          </div>
        </div>
      )
    }
  },


  render: function() {

    return (
      <div>
        {this.getLineupCards()}

        {this.getCreateLineupAd()}

        <LobbyDraftGroupSelectionModal
          ref="draftModal"
          draftGroupInfo={this.props.draftGroupInfo}
        />
      </div>
    );
  }
});


// Redux integration
let {Provider, connect} = ReactRedux;

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {
    lineups: LineupsBySportSelector(state),
    lineupsInfo: UpcomingLineupsInfo(state),
    focusedLineupId: state.upcomingLineups.focusedLineupId,
    draftGroupInfo: draftGroupInfoSelector(state),
    entries: state.entries.items
  };
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    fetchUpcomingLineups: () => dispatch(fetchUpcomingLineups()),
    lineupFocused: (lineupId) => dispatch(lineupFocused(lineupId)),
    fetchEntriesIfNeeded: () => dispatch(fetchEntriesIfNeeded())
  };
}

// Wrap the component to inject dispatch and selected state into it.
var LineupCardListConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(LineupCardList);

// Render the component.
renderComponent(
  <Provider store={store}>
    <LineupCardListConnected />
  </Provider>,
  '.cmp-lineup-card-list'
);


module.exports = LineupCardList;
