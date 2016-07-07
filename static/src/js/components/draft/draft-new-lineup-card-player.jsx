/* eslint no-param-reassign: 0 */
import React from 'react';
import { roundUpToDecimalPlace } from '../../lib/utils.js';


/**
 * An individual player row in the new lineup card in the draft section sidebar
 */
const DraftNewLineupCardPlayer = (props) => {
  if (props.player.player) {
    const names = props.player.player.name.split(' ');

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
          className="cmp-lineup-card__name-salary"
          onClick={props.onPlayerClick.bind(null, props.player.player.player_id)}
        >
          <span className="name">
            {names[0][0]}. {names[names.length - 1]}
            <span className="cmp-lineup-card__team">- {props.player.player.team_alias}</span>
          </span>
          <span className="salary">{roundUpToDecimalPlace(props.player.player.fppg, 1)} Avg</span>
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
};

module.exports = DraftNewLineupCardPlayer;
