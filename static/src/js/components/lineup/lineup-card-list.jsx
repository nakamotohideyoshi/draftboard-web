'use strict';

var React = require('react');
var LineupCard = require('./lineup-card.jsx');
var renderComponent = require('../../lib/render-component');
var smoothScrollTo = require('../../lib/smooth-scroll-to.js');

/**
 * Renders a list of lineup cards. Feed it lineup data and it will render LineupCard components for
 * each lineup.
 */
var LineupCardList = React.createClass({

  propTypes: {
    lineups: React.PropTypes.array
  },

  getDefaultProps: function(){
    // Since we don't have real data yet, add some empty lineups and let the LineupCard render
    // whatever it likes.
    return {
      lineups: [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
    };
  },

  getInitialState: function() {
    return {
      activeLineupId: 0
    };
  },

  /**
   * Smoothly scroll to a lineup card.
   * @param  {Object} cardDom DOM object of the card to be scrolled to.
   */
  scrollToCard: function(cardDom) {
    var scrollingElement = document.querySelector('.sidebar .sidebar-inner');
    smoothScrollTo(scrollingElement, cardDom.offsetTop - 20, 600);
  },

  /**
   * Set a lineupCard as being 'active' - this un-collapses and scrolls to it.
   * @param  {int}   lineupId   The ID of the lineup.
   * @param  {Function} callback a callback to be done after the lineup is set as active
   *                    (and expanded).
   */
  setActiveLineup: function(lineupId, callback) {
    return this.setState({
      activeLineupId: lineupId
    }, callback);
  },

  /**
   * Click handler for a lineupCard
   * @param  {Object} lineupCard the lineupCard react component.
   * @param  {int} id The cards ID TODO: this can be removed once we have legit data.
   */
  onCardClick: function(lineupCard, id) {
    // We need to wait until the lineup has been activated before it is scrolled to because if the
    // previously activated lineup is above it in the list, the offset dimensions change when it
    // collapses. Pass it as a callback that eventually gets used as a setState() callback.
    this.setActiveLineup(id, function() {
      this.scrollToCard(lineupCard.getDOMNode());
    });
  },

  render: function() {
    var lineups = this.props.lineups.map(function(lineup, i) {
      return (
        <LineupCard
          key={i}
          lineup={lineup}
          isActive={this.state.activeLineupId === i}
          onCardClick={this.onCardClick}
          tempId={i}
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
