import React from 'react';
import ReactDom from 'react-dom';
import * as ReactRedux from 'react-redux';
import { find as _find } from 'lodash';
import store from '../../store';
import LineupCard from '../lineup/lineup-card.jsx';
import renderComponent from '../../lib/render-component';
import smoothScrollTo from '../../lib/smooth-scroll-to.js';
import LobbyDraftGroupSelectionModal from './lobby-draft-group-selection-modal.jsx';
import { fetchUpcomingLineups, lineupFocused, lineupHovered } from '../../actions/lineup-actions.js';
import { openDraftGroupSelectionModal, closeDraftGroupSelectionModal, } from
  '../../actions/upcoming-draft-groups-actions.js';
import { draftGroupInfoSelector } from '../../selectors/draft-group-info-selector.js';
import { lineupsBySportSelector } from '../../selectors/upcoming-lineups-by-sport.js';
import { upcomingLineupsInfo } from '../../selectors/upcoming-lineups-info.js';
import '../contest-list/contest-list-sport-filter.jsx';
const { Provider, connect } = ReactRedux;


/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
function mapStateToProps(state) {
  return {
    lineups: lineupsBySportSelector(state),
    lineupsInfo: upcomingLineupsInfo(state),
    focusedLineupId: state.upcomingLineups.focusedLineupId,
    draftGroupInfo: draftGroupInfoSelector(state),
    draftGroupSelectionModalIsOpen: state.upcomingDraftGroups.draftGroupSelectionModalIsOpen,
    entries: state.entries.items,
  };
}

/*
 * Map Redux actions to React component properties
 * @param  {function} dispatch The dispatch method to pass actions into
 * @return {object}            All of the methods to map to the component
 */
function mapDispatchToProps(dispatch) {
  return {
    fetchUpcomingLineups: () => dispatch(fetchUpcomingLineups()),
    lineupFocused: (lineupId) => dispatch(lineupFocused(lineupId)),
    lineupHovered: (lineupId) => dispatch(lineupHovered(lineupId)),
    openDraftGroupSelectionModal: () => dispatch(openDraftGroupSelectionModal()),
    closeDraftGroupSelectionModal: () => dispatch(closeDraftGroupSelectionModal()),
  };
}


/**
 * Renders a list of lineup cards. Feed it lineup data and it will render LineupCard components for
 * each lineup.
 */
const LineupCardList = React.createClass({

  propTypes: {
    lineupFocused: React.PropTypes.func,
    lineupHovered: React.PropTypes.func,
    fetchUpcomingLineups: React.PropTypes.func.isRequired,
    lineups: React.PropTypes.array.isRequired,
    lineupsInfo: React.PropTypes.object,
    focusedLineupId: React.PropTypes.number,
    draftGroupInfo: React.PropTypes.object,
    openDraftGroupSelectionModal: React.PropTypes.func,
    closeDraftGroupSelectionModal: React.PropTypes.func,
    draftGroupSelectionModalIsOpen: React.PropTypes.bool,
  },

  getDefaultProps() {
    return {
      lineups: [],
    };
  },


  componentWillMount() {
    if (window.dfs.user.isAuthenticated === true) {
      this.props.fetchUpcomingLineups();
    }
  },


  componentDidUpdate(prevProps) {
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
  onCardClick(lineup) {
    this.setActiveLineup(lineup.id);
    this.props.lineupHovered(null);
  },


  /**
   * Set a lineupCard as being 'focused' - this un-collapses and scrolls to it.
   * @param  {int}   lineupId   The ID of the lineup.
   */
  setActiveLineup(lineupId) {
    this.props.lineupFocused(lineupId);
  },


  getLineupCards() {
    return this.props.lineups.map((lineup) => {
      // We'll need a reference to the card in order to get it's DOM element and scroll to it when
      // it gets focused.
      const refName = `lineup-${lineup.id}`;
      const lineupInfo = _find(this.props.lineupsInfo, { id: lineup.id });
      const draftGroupInfo = _find(this.props.draftGroupInfo.draftGroups, { pk: lineup.draft_group });
      let entries;
      let fees;

      if (lineupInfo) {
        fees = lineupInfo.fees;
        entries = lineupInfo.entries;
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
          onHover={this.handleLineupHovered}
        />
      );
    }, this);
  },


  getCreateLineupAd() {
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
      );
    }

    return (
      <div className="cmp-lineup-card cmp-lineup-card--create cmp-lineup-card--create__nba">
        <header className="cmp-lineup-card__header">
          <h3 className="cmp-lineup-card__title">
            <span>It’s <br />Anyone’s<br /> Game.</span>
          </h3>
        </header>

        <div
          className="button button--medium button--gradient-outline"
          onClick={this.handleDraftButtonClick}
        >
          Start Drafting <span className="right">→</span>
        </div>
      </div>
    );
  },


  handleLineupHovered(lineupId) {
    this.props.lineupHovered(lineupId);
  },


  handleDraftButtonClick() {
    this.props.openDraftGroupSelectionModal();
  },


  /**
   * Smoothly scroll to a lineup card.
   * @param  {int} the id of the lineup to scroll to.
   */
  scrollToCard(lineupId) {
    const cardDom = ReactDom.findDOMNode(this.refs[`lineup-${lineupId}`]);

    if (cardDom) {
      const scrollingElement = document.querySelector('.sidebar .sidebar-inner');
      smoothScrollTo(scrollingElement, cardDom.offsetTop - 20, 600);
    }
  },


  render() {
    return (
      <div>
        {this.getLineupCards()}

        {this.getCreateLineupAd()}

        <LobbyDraftGroupSelectionModal
          ref="draftModal"
          draftGroupInfo={this.props.draftGroupInfo}
          onClose={this.props.closeDraftGroupSelectionModal}
          isOpen={this.props.draftGroupSelectionModalIsOpen}
        />
      </div>
    );
  },
});


// Wrap the component to inject dispatch and selected state into it.
const LineupCardListConnected = connect(
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
