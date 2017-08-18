import React from 'react';
import moment from 'moment';

// These need to match up with the playerPositionFilters in draft-container.jsx in order
// to filter properly when the row is clicked.
const playerPlaceHolder = [
  // NFL
  { position: 'QB', placeholder: 'Select a Quarterback' },
  { position: 'RB', placeholder: 'Select a Running Back' },
  { position: 'WR', placeholder: 'Select a Wide Receiver' },
  { position: 'TE', placeholder: 'Select a Tight End' },
  { position: 'FX', placeholder: 'Select a RB, WR, or TE' },
  // MLB
  { position: 'SP', placeholder: 'Select a Pitcher' },
  { position: 'C', placeholder: 'Select a Catcher' },
  { position: '1B', placeholder: 'Select a First Baseman' },
  { position: '2B', placeholder: 'Select a Second Baseman' },
  { position: '3B', placeholder: 'Select a Third Baseman' },
  { position: 'SS', placeholder: 'Select a Shortstop' },
  { position: 'OF', placeholder: 'Select an Outfielder' },
  { position: 'OF', placeholder: 'Select an Outfielder' },
  { position: 'OF', placeholder: 'Select an Outfielder' },
];

const getDefaultPlaceholder = (pos) => {
  for (let i = 0; i < playerPlaceHolder.length; i++) {
    if (playerPlaceHolder[i].position === pos) {
      return playerPlaceHolder[i].placeholder;
    }
  }
};

const getFormattedGame = (gameSrid, playerTeamSrid, draftGroupBoxScores) => {
  const formatTeam = (playerTeam, teamSrid, teamName) => {
    if (playerTeam && teamSrid) {
      let classname = '';
      if (playerTeam === teamSrid) {
        classname = 'players-team';
      }

      return <span className={classname}>{teamName}</span>;
    }

    return <span></span>;
  };

  if (draftGroupBoxScores.hasOwnProperty(gameSrid)) {
    const game = draftGroupBoxScores[gameSrid];

    return (
      <div>
        {formatTeam(playerTeamSrid, game.srid_away, game.away_team)} @&nbsp;
        {formatTeam(playerTeamSrid, game.srid_home, game.home_team)}&nbsp;
        {moment(game.start, moment.ISO_8601).format('h:mma')}
      </div>
    );
  }
  return '';
};


/**
 * An individual player row in the new lineup card in the draft section sidebar
 */
const DraftNewLineupCardPlayer = (props) => {
  if (props.player.player) {
    /* eslint no-param-reassign: 0 */
    return (
      <li className="cmp-lineup-card__player occupied" key={props.player.idx}>
        <span className="cmp-lineup-card__position">{props.player.name}</span>
        <div className="circle">
          <span
            className="cmp-lineup-card__photo"
            style={{ backgroundImage: `url(${props.playerImagesBaseUrl}/120/${props.player.player.player_srid}.png)` }}
            onError={(tag) => {
              tag.currentTarget.style.backgroundImage = require('../../../img/blocks/draft-list/lineup-no-player.png');
            }}
          >
          </span>
        </div>


        <span
          className="cmp-lineup-card__name-game"
          onClick={props.onPlayerClick.bind(null, props.player.player.player_id)}
        >
          <span className="name">
            {props.player.player.name}
          </span>

          <span className="game">
            {getFormattedGame(
              props.player.player.game_srid,
              props.player.player.team_srid,
              props.draftGroupBoxScores
            )}
            </span>
        </span>

        <span className="cmp-lineup-card__average">
          <span className="text">${props.player.player.salary.toLocaleString('en')}</span>
        </span>

        <span
          className="cmp-lineup-card__delete"
          onClick={props.removePlayer.bind(null, props.player.player.player_id)}
        >
          <div className="icon"></div>
        </span>
      </li>
    );
    /* eslint-enable no-param-reassign */
  }

  return (
    <li className="cmp-lineup-card__player vacant" key={props.player.idx}>
      <span className="cmp-lineup-card__position">{props.player.name}</span>
      <div className="circle">
        <span
          className="cmp-lineup-card__photo"
          style={{ backgroundImage: `url(${require('../../../img/blocks/draft-list/lineup-no-player.png')})` }}
        >

        </span>
      </div>

      <span className="cmp-lineup-card__name-game">
        <span className="name">
          <span
            className="placeholder"
            onClick={props.onEmtpySlotClick.bind(null, props.player.name)}
          >
              {getDefaultPlaceholder(props.player.name)}
          </span>
          <span className="cmp-lineup-card__team">&nbsp;</span>
        </span>
        <span className="salary">&nbsp;</span>
      </span>

      <span className="cmp-lineup-card__average">&nbsp;</span>
    </li>
  );
};


DraftNewLineupCardPlayer.propTypes = {
  // A player row object.
  player: React.PropTypes.object.isRequired,
  playerImagesBaseUrl: React.PropTypes.string.isRequired,
  // What happens when the delete button is clicked.
  removePlayer: React.PropTypes.func.isRequired,
  onPlayerClick: React.PropTypes.func.isRequired,
  // When an empty slot "Select a Quarterback" is clicked.
  onEmtpySlotClick: React.PropTypes.func.isRequired,
  draftGroupBoxScores: React.PropTypes.object.isRequired,
};

module.exports = DraftNewLineupCardPlayer;
