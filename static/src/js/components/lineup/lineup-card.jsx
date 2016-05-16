import React from 'react';
import LineupCardPlayer from './lineup-card-player.jsx';
import CountdownClock from '../site/countdown-clock.jsx';
import LineupCardEntries from './lineup-card-entries.jsx';


const LineupCard = React.createClass({

  propTypes: {
    isActive: React.PropTypes.bool,
    onCardClick: React.PropTypes.func.isRequired,
    lineup: React.PropTypes.object.isRequired,
    lineupInfo: React.PropTypes.object.isRequired,
    hoverText: React.PropTypes.string,
    draftGroupInfo: React.PropTypes.object.isRequired,
    onHover: React.PropTypes.func,
    removeContestPoolEntry: React.PropTypes.func.isRequired,
  },


  getDefaultProps() {
    return ({
      hoverText: 'Select This Lineup',
      draftGroupInfo: {},
      onHover: () => ({}),
    });
  },


  getInitialState() {
    return {
      flipped: false,
    };
  },


  componentDidMount() {
    this.setCardHeight();
  },


  componentDidUpdate() {
    this.setCardHeight();
  },


  // Because of the 3D transform, we have to manually set the height of the card back.
  // Run this on componentDidMount & componentDidUpdate.
  setCardHeight() {
    if (this.refs.back && this.refs.front) {
      this.refs.back.style.height = `${this.refs.front.clientHeight}px`;
    }
  },


  flipCard() {
    this.setState({
      flipped: !this.state.flipped,
    });
  },


  // Toggle the visibility of the tooltip.
  showControls() {
    this.refs.lineupCardTip.toggle();
  },


  render() {
    let lineup = '';

    /**
     * If the lineup card is active, show the expanded state with player details.
     */
    if (this.props.isActive) {
      const flippedClass = this.state.flipped ? 'flipped' : '';
      const playerImagesBaseUrl = `${window.dfs.playerImagesBaseUrl}/${this.props.lineup.sport}`;
      const players = this.props.lineup.players.map((player) => (
        <LineupCardPlayer
          player={player}
          key={player.player_id}
          playerImagesBaseUrl={playerImagesBaseUrl}
        />
      ));

      lineup = (
        <div className={`cmp-lineup-card cmp-lineup-card--expanded flip-container ${flippedClass}`}>
          <div className="flipper">
            <div className="front" ref="front">
              <header className="cmp-lineup-card__header">
                <h3 className="cmp-lineup-card__title">
                  {this.props.lineup.name || `Untitled Lineup # ${this.props.lineup.id}`}
                </h3>

                <div className="actions-menu-container">
                <ul className="actions">
                  <li>
                    <a
                      className="icon-edit action"
                      href={`/draft/${this.props.lineup.draft_group}/lineup/${this.props.lineup.id}/edit/`}
                    ></a>
                  </li>

                  <li>
                    <div
                      className="icon-flip action"
                      onClick={this.flipCard}
                    ></div>
                  </li>
                </ul>
                </div>
              </header>

              <div className="cmp-lineup-card__list-header">
                <span className="cmp-lineup-card__list-header-salary">Salary</span>
              </div>

              <ul className="players">
                {players}
              </ul>

              <footer className="cmp-lineup-card__footer">
                <div className="cmp-lineup-card__fees cmp-lineup-card__footer-section">
                  <span className="cmp-lineup-card__footer-title">Fees</span>
                ${this.props.lineupInfo.fees}
                </div>

                <div className="cmp-lineup-card__countdown cmp-lineup-card__footer-section">
                  <span className="cmp-lineup-card__footer-title">Live In</span>
                  <CountdownClock time={this.props.draftGroupInfo.start} />
                </div>

                <div className="cmp-lineup-card__entries cmp-lineup-card__footer-section">
                  <span className="cmp-lineup-card__footer-title">Entries</span>
                {this.props.lineupInfo.totalEntryCount}
                </div>
              </footer>
            </div>

            <div className="back" ref="back">
              <LineupCardEntries
                lineupInfo={this.props.lineupInfo}
                flipCard={this.flipCard}
                removeContestPoolEntry={this.props.removeContestPoolEntry}
              />
            </div>
          </div>

        </div>
      );
    } else {
      /**
       * If it is not the active lineup, only show the lineup title.
       */
      lineup = (
        <div
          className="cmp-lineup-card cmp-lineup-card--collapsed"
          onClick={this.props.onCardClick.bind(null, this.props.lineup)}
          onMouseOver={this.props.onHover.bind(null, this.props.lineup.id)}
          onMouseOut={this.props.onHover.bind(null, null)}
        >
          <header className="cmp-lineup-card__header">
            <h3 className="cmp-lineup-card__title">
              {this.props.lineup.name || `Untitled Lineup # ${this.props.lineup.id}`}
            </h3>
          </header>
          <div className="cmp-lineup-card__select">
            <h4>{this.props.hoverText}</h4>
          </div>
        </div>
      );
    }

    return (
      lineup
    );
  },

});


module.exports = LineupCard;
