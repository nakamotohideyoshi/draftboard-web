/* eslint no-param-reassign: 0 */
import React from 'react';
import moment from 'moment';
import find from 'lodash/find';


const getFormattedGame = (playerTeamSrid, boxScores) => {
  const playerIsHome = find(boxScores, {
    srid_home: playerTeamSrid,
  });

  const playerIsAway = find(boxScores, {
    srid_away: playerTeamSrid,
  });

  const game = playerIsHome || playerIsAway;

  const formatTeam = (playerTeam, teamSrid, teamName) => {
    let classname = '';
    if (playerTeam === teamSrid) {
      classname = 'players-team';
    }

    return <span className={classname}>{teamName}</span>;
  };

  if (game) {
    // Return the formatted info
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
 * A player row to be placed in a lineup card.
 */
const LineupCardPlayer = (props) => (
  <li className="cmp-lineup-card__player">
    <span className="cmp-lineup-card__position">{props.player.roster_spot}</span>
    <span className="cmp-lineup-card__photo">
      <img
        src={`${props.playerImagesBaseUrl}/120/${props.player.player_meta.srid}.png`}
        onError={(tag) => {
          tag.currentTarget.src = require('../../../img/blocks/draft-list/lineup-no-player.png');
        }}
        alt=""
        width="auto"
        height="35px"
      />
    </span>
    <span className="cmp-lineup-card__name-game">
      <span className="name">{props.player.player_meta.first_name} {props.player.player_meta.last_name}</span>
      <span className="game">
        {getFormattedGame(props.player.player_meta.team.srid, props.draftGroupInfo.boxScores)}
      </span>
    </span>
    <span className="cmp-lineup-card__average">
      <span className="text">${ props.player.salary.toLocaleString('en') }</span>
    </span>
  </li>
);

LineupCardPlayer.propTypes = {
  player: React.PropTypes.object.isRequired,
  playerImagesBaseUrl: React.PropTypes.string.isRequired,
  draftGroupInfo: React.PropTypes.object.isRequired,
};

module.exports = LineupCardPlayer;
