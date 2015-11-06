const React = require('react');
const ReactRedux = require('react-redux');
const store = require('../../store');
const LineupCard = require('../lineup/lineup-card.jsx');
const renderComponent = require('../../lib/render-component');
const smoothScrollTo = require('../../lib/smooth-scroll-to.js');
const DraftGroupSelectionModal = require('./lobby-draft-group-selection-modal.jsx');
import {fetchUpcomingLineups, lineupFocused} from '../../actions/lineup-actions.js';


/**
 * Renders a list of lineup cards. Feed it lineup data and it will render LineupCard components for
 * each lineup.
 */
var LineupCardList = React.createClass({

  getInitialState: function() {
    return {
      lineups: [],
      focusedLineupId: 10,
      draftGroupSelectionModalVisible: false
    };
  },


  /**
   * Smoothly scroll to a lineup card.
   * @param  {int} the id of the lineup to scroll to.
   */
  scrollToCard: function(lineupId) {
    var cardDom = React.findDOMNode(this.refs['lineup-' + lineupId]);

    if (cardDom) {
      var scrollingElement = document.querySelector('.sidebar .sidebar-inner');
      smoothScrollTo(scrollingElement, cardDom.offsetTop - 20, 600);
    }
  },


  /**
   * Set a lineupCard as being 'focused' - this un-collapses and scrolls to it.
   * @param  {int}   lineupId   The ID of the lineup.
   */
  setActiveLineup: function(lineupId) {
    lineupFocused(lineupId);
  },


  componentDidUpdate: function(prevProps, prevState) {
    // We need to wait until the lineup has been activated before it is scrolled to because if the
    // previously activated lineup is above it in the list, the offset dimensions change when it
    // collapses. This will wait until the DOM has been updated and the old focused lineup has
    // collapsed.
    if (this.state.focusedLineupId !== prevState.focusedLineupId) {
      this.scrollToCard(this.state.focusedLineupId);
    }
  },


  /**
   * Click handler for a lineupCard
   * @param  {int} id The cards ID TODO: this can be removed once we have legit data.
   */
  onCardClick: function(id) {
    this.setActiveLineup(id);
  },


  handleDraftButtonClick: function() {
    this.refs.draftModal.open();
  },


  render: function() {

    var lineups = this.state.lineups.map(function(lineup) {
      // We'll need a reference to the card in order to get it's DOM element and scroll to it when
      // it gets focused.
      var refName = 'lineup-' + lineup.id;

      return (
        <LineupCard
          key={lineup.id}
          lineup={lineup}
          isActive={this.state.focusedLineupId === lineup.id}
          ref={refName}
          onCardClick={this.onCardClick}
        />
      );
    }, this);

    return (
      <div>
        {lineups}

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

        <DraftGroupSelectionModal
          ref="draftModal"
        />
      </div>
    );
  }
});


// =============================================================================
// Redux integration
let {Provider, connect} = ReactRedux;

// Which part of the Redux global state does our component want to receive as props?
function mapStateToProps(state) {
  return {
  };
}

// Which action creators does it want to receive by props?
function mapDispatchToProps(dispatch) {
  return {
    fetchUpcomingLineups,
    lineupFocused: (lineupId) => dispatch(lineupFocused(lineupId))
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
