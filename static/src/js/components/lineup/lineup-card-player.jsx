/* eslint no-param-reassign: 0 */
import React from 'react';


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
          tag.currentTarget.src = '/static/src/img/blocks/draft-list/lineup-no-player.png';
        }}
        width="auto"
        height="35px"
      />
    </span>
    <span className="cmp-lineup-card__name">
      {props.player.player_meta.first_name[0]}.
      {props.player.player_meta.last_name}
      <span className="cmp-lineup-card__team">
        - {props.player.player_meta.team.alias}
      </span>
    </span>
    <span className="cmp-lineup-card__salary">${props.player.salary.toLocaleString('en')}</span>
  </li>
);

LineupCardPlayer.propTypes = {
  player: React.PropTypes.object.isRequired,
  playerImagesBaseUrl: React.PropTypes.string.isRequired,
};

module.exports = LineupCardPlayer;
