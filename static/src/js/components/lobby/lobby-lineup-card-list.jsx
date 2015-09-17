'use strict';

var React = require('react');
var Reflux = require('reflux');
var LineupCard = require('../lineup/lineup-card.jsx');
var renderComponent = require('../../lib/render-component');
var smoothScrollTo = require('../../lib/smooth-scroll-to.js');
var LineupStore = require('../../stores/lineup-store.js');
var LineupActions = require('../../actions/lineup-actions.js');


/**
 * Renders a list of lineup cards. Feed it lineup data and it will render LineupCard components for
 * each lineup.
 */
var LineupCardList = React.createClass({

  mixins: [
    Reflux.connect(LineupStore)
  ],


  getInitialState: function() {
    return {
      lineups: [],
      focusedLineupId: 10
    };
  },


  /**
   * Smoothly scroll to a lineup card.
   * @param  {int} the id of the lineup to scroll to.
   */
  scrollToCard: function(lineupId) {
    var cardDom = React.findDOMNode(this.refs['lineup-' + lineupId]);
    var scrollingElement = document.querySelector('.sidebar .sidebar-inner');
    smoothScrollTo(scrollingElement, cardDom.offsetTop - 20, 600);
  },


  /**
   * Set a lineupCard as being 'focused' - this un-collapses and scrolls to it.
   * @param  {int}   lineupId   The ID of the lineup.
   */
  setActiveLineup: function(lineupId) {
    LineupActions.lineupFocused(lineupId);
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

        <div className="cmp-lineup-card cmp-lineup-card--collapsed cmp-lineup-card--create-collapsed">
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

          <div className="button button--medium button--gradient-outline">Draft a Team</div>
        </div>
      </div>


    );
  }
});

// Render the component.
renderComponent(<LineupCardList />, '.cmp-lineup-card-list');


module.exports = LineupCardList;
