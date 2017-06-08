import React from 'react';
import ReactDom from 'react-dom';
import * as ReactRedux from 'react-redux';
import { push as routerPush } from 'react-router-redux';
import find from 'lodash/find';
import log from '../../lib/logging';
import store from '../../store';
import LineupCard from '../lineup/lineup-card';
import renderComponent from '../../lib/render-component';
import smoothScrollTo from '../../lib/smooth-scroll-to';
import LobbyDraftGroupSelectionModal from './lobby-draft-group-selection-modal';
import { fetchUpcomingLineups, lineupFocused, lineupHovered } from '../../actions/upcoming-lineup-actions';
import { openDraftGroupSelectionModal, closeDraftGroupSelectionModal } from
  '../../actions/upcoming-draft-groups-actions';
import { removeContestPoolEntry } from '../../actions/contest-pool-actions';
import { draftGroupInfoSelector } from '../../selectors/draft-group-info-selector';
import { lineupsBySportSelector } from '../../selectors/upcoming-lineups-by-sport';
import { focusedContestInfoSelector } from '../../selectors/lobby-selectors';
import { upcomingLineupsInfo } from '../../selectors/upcoming-lineups-info';
import SelectDraftGroupButton from './select-draft-group-button';
import '../contest-list/contest-list-sport-filter';
import { removeParamFromURL } from '../../lib/utils';

const { Provider, connect } = ReactRedux;


/*
 * Map selectors to the React component
 * @param  {object} state The current Redux state that we need to pass into the selectors
 * @return {object}       All of the methods we want to map to the component
 */
function mapStateToProps(state) {
  return {
    draftGroupInfo: draftGroupInfoSelector(state),
    draftGroupSelectionModalIsOpen: state.upcomingDraftGroups.draftGroupSelectionModalIsOpen,
    focusedContestInfo: focusedContestInfoSelector(state),
    focusedLineupId: state.upcomingLineups.focusedLineupId,
    focusedSport: state.contestPools.filters.sportFilter.match,
    lineups: lineupsBySportSelector(state),
    lineupsInfo: upcomingLineupsInfo(state),
    queryLineup: state.routing.locationBeforeTransitions.query.lineup,
  };
}

/*
 * Map Redux actions to React component properties
 * @param  {function} dispatch The dispatch method to pass actions into
 * @return {object}            All of the methods to map to the component
 */
function mapDispatchToProps(dispatch) {
  return {
    closeDraftGroupSelectionModal: () => dispatch(closeDraftGroupSelectionModal()),
    fetchUpcomingLineups: () => dispatch(fetchUpcomingLineups()),
    lineupFocused: (lineupId) => dispatch(lineupFocused(lineupId)),
    lineupHovered: (lineupId) => dispatch(lineupHovered(lineupId)),
    openDraftGroupSelectionModal: () => dispatch(openDraftGroupSelectionModal()),
    removeContestPoolEntry: (entry) => dispatch(removeContestPoolEntry(entry)),
    routerPush: (path) => dispatch(routerPush(path)),
  };
}


/**
 * Renders a list of lineup cards. Feed it lineup data and it will render LineupCard components for
 * each lineup.
 */
const LineupCardList = React.createClass({

  propTypes: {
    closeDraftGroupSelectionModal: React.PropTypes.func,
    draftGroupInfo: React.PropTypes.object,
    draftGroupSelectionModalIsOpen: React.PropTypes.bool,
    fetchUpcomingLineups: React.PropTypes.func.isRequired,
    focusedContestInfo: React.PropTypes.object,
    focusedLineupId: React.PropTypes.number,
    focusedSport: React.PropTypes.string.isRequired,
    lineupFocused: React.PropTypes.func,
    lineupHovered: React.PropTypes.func,
    lineups: React.PropTypes.array.isRequired,
    lineupsInfo: React.PropTypes.object,
    openDraftGroupSelectionModal: React.PropTypes.func.isRequired,
    queryLineup: React.PropTypes.string,
    removeContestPoolEntry: React.PropTypes.func.isRequired,
    routerPush: React.PropTypes.func,
  },

  getDefaultProps() {
    return {
      lineups: [],
    };
  },


  componentWillMount() {
    if (window.dfs.user.isAuthenticated === true) {
      return this.props.fetchUpcomingLineups().then(() => {
        // if a lineup id was in the query params it means it was just saved and we should focus it.
        if (this.props.queryLineup) {
          const lineupId = parseInt(this.props.queryLineup, 10);
          // make sure it's an integer.
          if (typeof lineupId === 'number' && (lineupId % 1) === 0) {
            log.info(`focusing lineup id: ${this.props.queryLineup}`);
            this.props.lineupFocused(lineupId);
            // Strip out the 'lineup' param from the url.
            const strippedParams = removeParamFromURL(window.location.search, 'lineup');
            this.props.routerPush(`/contests/${strippedParams}`);
          } else {
            log.warn(`lineup url param '${this.props.queryLineup}' is not an integer!`);
          }
        }

        return true;
      });
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
      const lineupInfo = find(this.props.lineupsInfo, { id: lineup.id });
      const draftGroupInfo = find(this.props.draftGroupInfo.draftGroups, { pk: lineup.draft_group });

      if (lineupInfo) {
        return (
          <LineupCard
            key={lineup.id}
            lineup={lineup}
            lineupInfo={lineupInfo}
            draftGroupInfo={draftGroupInfo}
            isActive={this.props.focusedLineupId === lineup.id}
            ref={refName}
            onCardClick={this.onCardClick}
            onHover={this.handleLineupHovered}
            removeContestPoolEntry={this.props.removeContestPoolEntry}
            focusedContestInfo={this.props.focusedContestInfo}
          />
        );
      }
    }, this);
  },


  getCreateLineupAd() {
    if (this.props.lineups.length > 0) {
      // If the user already has a lineup for this sport, don't show a create button.
      return '';
    }

    return (
      <div className="cmp-lineup-card cmp-lineup-card--create cmp-lineup-card--create__nba">
        <header className="cmp-lineup-card__header">
          <h3 className="cmp-lineup-card__title">
            <span>It’s <br />Anyone’s<br /> Game.</span>
          </h3>
        </header>

        <SelectDraftGroupButton
          draftGroupInfo={this.props.draftGroupInfo}
          focusedSport={this.props.focusedSport}
          onClick={this.props.openDraftGroupSelectionModal}
          title="CREATE A LINEUP"
        />
      </div>
    );
  },


  handleLineupHovered(lineupId) {
    this.props.lineupHovered(lineupId);
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
          focusedSport={this.props.focusedSport}
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
