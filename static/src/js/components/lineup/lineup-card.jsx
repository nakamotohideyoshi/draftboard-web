import React from 'react';
import LineupCardPlayer from './lineup-card-player.jsx';
import CountdownClock from '../site/countdown-clock.jsx';
import LineupCardEntries from './lineup-card-entries.jsx';
import classNames from 'classnames';
import SportIcon from '../site/sport-icon.jsx';


const LineupCard = React.createClass({

  propTypes: {
    isActive: React.PropTypes.bool,
    onCardClick: React.PropTypes.func.isRequired,
    lineup: React.PropTypes.object.isRequired,
    lineupInfo: React.PropTypes.object,
    hoverText: React.PropTypes.string,
    draftGroupInfo: React.PropTypes.object.isRequired,
    onHover: React.PropTypes.func,
    removeContestPoolEntry: React.PropTypes.func,
    focusedContestInfo: React.PropTypes.object,
  },


  getDefaultProps() {
    return ({
      hoverText: 'Select This Lineup',
      draftGroupInfo: {},
      lineupInfo: {},
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


  canEnterIntoFocusedContest(focusedContestInfo, lineup) {
    // If there is no focused contest, always return true.
    if (!focusedContestInfo || !focusedContestInfo.contest) {
      return true;
    }
    // If there are any entries, check if they are from the same lineup.
    // If not, then the lineup can not be entered into this contest.
    if (focusedContestInfo.contest.entryInfo &&
      focusedContestInfo.contest.entryInfo.length
    ) {
      return focusedContestInfo.contest.entryInfo[0].lineup === lineup.id;
    }

    // If there are no entries, check if the lineup is for the same draftgroup
    // as the contest pool.
    if (focusedContestInfo.contest.draft_group !== lineup.draft_group) {
      return false;
    }

    // Default to true.
    return true;
  },


  handleMouseOver(lineupId) {
    this.props.onHover(lineupId);
  },


  handleMouseOut() {
    this.props.onHover(null, null);
  },


  render() {
    // Add classes based on whether the focused contestpool can be entered into.
    const classes = classNames({
      'cannot-enter': !this.canEnterIntoFocusedContest(
                        this.props.focusedContestInfo,
                        this.props.lineup
                      ),
    });


    let lineup = '';

    /**
     * If the lineup card is active, show the expanded state with player details.
     */
    const flippedClass = this.state.flipped ? 'hover' : '';
    const playerImagesBaseUrl = `${window.dfs.playerImagesBaseUrl}/${this.props.lineup.sport}`;

    const players = this.props.lineup.players.map((player) => (
      <LineupCardPlayer
        player={player}
        key={player.player_id}
        playerImagesBaseUrl={playerImagesBaseUrl}
        draftGroupInfo={this.props.draftGroupInfo}
      />
    ));
    let classnames = 'cmp-lineup-card cmp-lineup-card--expanded flip-container';
    classnames += ` ${flippedClass} ${classes} ${this.props.lineup.sport}`;
    lineup = (
      <div className={classnames}>
        <div className="flipper">
          <div className="front" ref="front">
            <header className="cmp-lineup-card__header">
              <h3 className="cmp-lineup-card__title">
                <SportIcon sport={this.props.lineup.sport} />
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
              <div className="cmp-lineup-card__list-header">
              <span className="cmp-lineup-card__list-header-salary">Salary</span>
            </div>
            </header>
            <ul className="players">
              {players}
            </ul>

            <footer className="cmp-lineup-card__footer">
              <div className="cmp-lineup-card__countdown cmp-lineup-card__footer-section">
                <span className="cmp-lineup-card__footer-title">Live In</span>
                <CountdownClock time={this.props.draftGroupInfo.start} />
              </div>

              <div className="cmp-lineup-card__entries cmp-lineup-card__footer-section">
                <span className="cmp-lineup-card__footer-title">Fees</span>
                ${this.props.lineupInfo.fees}
              </div>

               <div className="cmp-lineup-card__entries cmp-lineup-card__footer-section">
                <span className="cmp-lineup-card__footer-title">Entries</span>
                {this.props.lineupInfo.totalEntryCount}
              </div>
            </footer>
          </div>

          <div className="back" ref="back">
            <header className="cmp-lineup-card__header">
              <h3 className="cmp-lineup-card__title">
                <SportIcon sport={this.props.lineupInfo.sport} />
                {this.props.lineupInfo.name || `Untitled Lineup # ${this.props.lineupInfo.id}`}
              </h3>

              <div className="actions-menu-container">
                <ul className="actions">
                  <li>
                    <div
                      className="icon-flop action"
                      onClick={this.flipCard}
                    ></div>
                  </li>
                </ul>
              </div>

              <div className="cmp-lineup-card__list-header">
                <span className="cmp-lineup-card__list-header-remove">Remove</span>
                <span className="cmp-lineup-card__list-header-contest">Contest</span>
                <span className="cmp-lineup-card__list-header-fee">Fee</span>
              </div>
            </header>

            <LineupCardEntries
              lineupInfo={this.props.lineupInfo}
              flipCard={this.flipCard}
              removeContestPoolEntry={this.props.removeContestPoolEntry}
              draftGroupInfo={this.props.draftGroupInfo}
            />

            <footer className="cmp-lineup-card__footer">
              <div className="cmp-lineup-card__countdown cmp-lineup-card__footer-section">
                <span className="cmp-lineup-card__footer-title">Live In</span>
                <CountdownClock time={this.props.draftGroupInfo.start} />
              </div>

              <div className="cmp-lineup-card__entries cmp-lineup-card__footer-section">
                <span className="cmp-lineup-card__footer-title">Fees / Entries</span>
                ${this.props.lineupInfo.fees} / {this.props.lineupInfo.totalEntryCount}
              </div>
            </footer>
          </div>
        </div>

      </div>
    );

    return (
      lineup
    );
  },

});


module.exports = LineupCard;
