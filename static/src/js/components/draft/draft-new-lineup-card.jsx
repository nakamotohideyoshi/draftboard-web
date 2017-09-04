import React from 'react';
import DraftNewLineupCardTitle from './draft-new-lineup-card-title.jsx';
import DraftNewLineupCardPlayer from './draft-new-lineup-card-player.jsx';
import forEach from 'lodash/forEach';
// import log from '../../lib/logging';
// import classnames from 'classnames';
import CardFooter from '../card/CardFooter';

const defaultLineupTitle = 'My Lineup';


/**
 * Lineup creation card on the sidebar of the draft page.
 */
const DraftNewLineupCard = React.createClass({

  propTypes: {
    isActive: React.PropTypes.bool,
    isSaving: React.PropTypes.bool,
    lineup: React.PropTypes.array.isRequired,
    lineupTitle: React.PropTypes.string,
    removePlayer: React.PropTypes.func.isRequired,
    remainingSalary: React.PropTypes.number,
    sport: React.PropTypes.string,
    avgRemainingPlayerSalary: React.PropTypes.number,
    errorMessage: React.PropTypes.oneOfType([React.PropTypes.array, React.PropTypes.string]),
    saveLineup: React.PropTypes.func.isRequired,
    handlePlayerClick: React.PropTypes.func,
    handleEmtpySlotClick: React.PropTypes.func,
    lineupCanBeSaved: React.PropTypes.bool,
    draftGroupBoxScores: React.PropTypes.object,
    draftGroupStart: React.PropTypes.string,
  },

  getDefaultProps() {
    return {
      lineup: [],
      remainingSalary: 0,
      avgRemainingPlayerSalary: 0,
      errorMessage: '',
    };
  },


  getInitialState() {
    return {
      lineupTitle: defaultLineupTitle,
    };
  },
  componentWillReceiveProps(nextProps) {
    if (nextProps.lineupTitle) {
      this.setState({ lineupTitle: nextProps.lineupTitle });
    }
  },


  setTitle(title) {
    this.state.lineupTitle = title;
  },


  saveLineup() {
    let title = this.state.lineupTitle;
    if (title === defaultLineupTitle) {
      title = '';
    }

    this.props.saveLineup(title);
  },


  // Toggle the visibility of the tooltip.
  showControls() {
    // this.refs.lineupCardTip.toggle();
  },


  renderErrors(errors) {
    if (errors === 'NEED_AUTH') {
      return (
        <span>
          Nice Lineup! Before we save it, you'll need to
          &nbsp;<a href={`/register/?next=${window.location.pathname}`}>register</a>
          &nbsp;or <a href={`/login/?next=${window.location.pathname}`}>log in</a>.
        </span>
      );
    }

    return forEach(errors, (error) => <span>{error}</span>);
  },


  renderSaveButton() {
    // If the lineup is being saved, disable the button.
    if (this.props.isSaving) {
      return (
        <span
          className="cmp-lineup-card__save button button--outline-alt1 buttom--sm button--disabled"
        >
          Save
        </span>
      );
    }

    if (this.props.lineupCanBeSaved) {
      return (
        <span
          className="cmp-lineup-card__save button button--gradient buttom--sm"
          onClick={this.saveLineup}
        >
          Save
        </span>
      );
    }

    return (
      <span
        className="cmp-lineup-card__save button button--outline-alt1 buttom--sm button--disabled"
        title="This lineup is incomplete."
      >
        Save
      </span>
    );
  },


  render() {
    const playerImagesBaseUrl = `${window.dfs.playerImagesBaseUrl}/${this.props.sport}`;
    const self = this;

    // const remainingSalaryClasses = classnames({
    //   negative: this.props.remainingSalary < 0,
    // });
    // const avgRemainingPlayerSalaryClasses = classnames({
    //   negative: this.props.avgRemainingPlayerSalary < 0,
    // });

    const players = this.props.lineup.map((player) => (
        <DraftNewLineupCardPlayer
          player={player}
          key={player.idx}
          removePlayer={self.props.removePlayer}
          onPlayerClick={self.props.handlePlayerClick}
          onEmtpySlotClick={self.props.handleEmtpySlotClick}
          playerImagesBaseUrl={playerImagesBaseUrl}
          draftGroupBoxScores={this.props.draftGroupBoxScores}
        />
      )
    );

    return (
      <div className="cmp-lineup-card cmp-lineup-card--new flip-container">
        <div className="flipper">
          <div className="front">
            <header className="cmp-lineup-card__header clearfix" onClick={this.showControls}>

              <DraftNewLineupCardTitle
                title={this.state.lineupTitle}
                setTitle={this.setTitle}
              />

              {this.renderSaveButton()}

              <div className="cmp-lineup-card__list-header">
                <span className="cmp-lineup-card__list-header-salary">Salary</span>
              </div>
            </header>
            <ul className="players">
              {players}
            </ul>
            <CardFooter
              start={this.props.draftGroupStart}
              remsalary={this.props.remainingSalary.toLocaleString('en')}
              playeravg={this.props.avgRemainingPlayerSalary.toLocaleString('en')}
            />
          </div>
        </div>
      </div>
    );
  },

});


module.exports = DraftNewLineupCard;
