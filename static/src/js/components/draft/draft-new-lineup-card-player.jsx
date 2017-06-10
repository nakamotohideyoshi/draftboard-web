/* eslint no-param-reassign: 0 */
import React from 'react';
import moment from 'moment';


const getFormattedGame = (gameSrid, playerTeamSrid, draftGroupBoxScores) => {
  const formatTeam = (playerTeam, team) => {
    let classname = '';
    if (playerTeam === team.srid) {
      classname = 'players-team';
    }

    return <span className={classname}>{team.alias}</span>;
  };


  if (gameSrid in draftGroupBoxScores) {
    const game = draftGroupBoxScores[gameSrid];

    return (
      <div>
        {formatTeam(playerTeamSrid, game.awayTeam)} @&nbsp;
        {formatTeam(playerTeamSrid, game.homeTeam)}&nbsp;
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
    return (
      <li className="cmp-lineup-card__player occupied" key={props.player.idx}>
        <span className="cmp-lineup-card__position">{props.player.name}</span>
        <span className="cmp-lineup-card__photo">
          <img
            src={`${props.playerImagesBaseUrl}/120/${props.player.player.player_srid}.png`}
            onError={(tag) => {
              tag.currentTarget.src = require('../../../img/blocks/draft-list/lineup-no-player.png');
            }}
            alt=""
            width="auto"
            height="35px"
          />
        </span>
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
  }

  return (
    <li className="cmp-lineup-card__player vacant" key={props.player.idx}>
      <span className="cmp-lineup-card__position">{props.player.name}</span>
      <span className="cmp-lineup-card__photo">
        <img
          alt="No Player Chosen"
          src={require('../../../img/blocks/draft-list/lineup-no-player.png')}
          width="auto"
          height="35px"
        />
      </span>
      <span className="cmp-lineup-card__name-salary">
        <span className="name">
          &nbsp;
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
  onPlayerClick: React.PropTypes.func,
  draftGroupBoxScores: React.PropTypes.object,
};

module.exports = DraftNewLineupCardPlayer;
