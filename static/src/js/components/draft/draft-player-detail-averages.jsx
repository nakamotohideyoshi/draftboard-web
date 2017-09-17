import React from 'react';
import { roundUpToDecimalPlace } from '../../lib/utils';

/**
 * Show a player's season averages (or is it last 10 game averages?). This sits
 * directly below the player images on the player detail panel in the draft
 * section.
 */
const DraftPlayerDetailAverages = (props) => {
  // If there is no boxscore history
  if (
    !props.player ||
    !props.player.boxScoreHistory ||
    !Object.keys(props.player.boxScoreHistory).length
  ) {
    return (
      <div className="player-stats">
          <div className="stat-section">
            <h6 className="stats-section__title">Season stats unavailable</h6>
          </div>
      </div>
    );
  }

  const bsh = props.player.boxScoreHistory || {};

  switch (props.player.sport) {
    /**
     * NFL
     */
    case 'nfl': {
      // QB
      if (props.player.position === 'QB') {
        return (
          <div className="player-stats">
            <div className="stat-section">
              <h6 className="stats-section__title">Passing Avg</h6>
              <ul>
                <li>
                  <div className="stat-name">YDS</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(bsh.avg_pass_yds, 1)}
                  </div>
                </li>
                <li>
                  <div className="stat-name">TD</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(bsh.avg_pass_td, 1)}
                  </div>
                </li>
                <li>
                  <div className="stat-name">INT</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(bsh.avg_pass_int, 1)}
                  </div>
                </li>
              </ul>
            </div>

            <div className="stat-section">
              <h6 className="stats-section__title">Rushing Avg</h6>
              <ul>
                <li>
                  <div className="stat-name">YDS</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(bsh.avg_rush_yds, 1)}
                  </div>
                </li>
                <li>
                  <div className="stat-name">TD</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(bsh.avg_rush_td, 1)}
                  </div>
                </li>
              </ul>
            </div>

            <div className="stat-section">
              <h6 className="stats-section__title">&nbsp;</h6>
              <ul>
                <li>
                  <div className="stat-name">FUM</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(bsh.avg_off_fum_lost, 1)}
                  </div>
                </li>
                <li>
                  <div className="stat-name">FP</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(props.player.season_fppg, 1)}
                  </div>
                </li>
              </ul>
            </div>
          </div>
        );
      }

      // RB
      if (props.player.position === 'RB') {
        return (
          <div className="player-stats">
            <div className="stat-section">
              <h6 className="stats-section__title">Rushing Avg</h6>
              <ul>
                <li>
                  <div className="stat-name">YDS</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(bsh.avg_rush_yds, 1)}
                  </div>
                </li>
                <li>
                  <div className="stat-name">TD</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(bsh.avg_rush_td, 1)}
                  </div>
                </li>
              </ul>
            </div>

            <div className="stat-section">
              <h6 className="stats-section__title">Receiving Avg</h6>
              <ul>
              <li>
                <div className="stat-name">REC</div>
                <div className="stat-score">
                  {roundUpToDecimalPlace(bsh.avg_rec_rec, 1)}
                </div>
              </li>

                <li>
                  <div className="stat-name">YDS</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(bsh.avg_rec_yds, 1)}
                  </div>
                </li>
                <li>
                  <div className="stat-name">TD</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(bsh.avg_rec_td, 1)}
                  </div>
                </li>
              </ul>
            </div>

            <div className="stat-section">
              <h6 className="stats-section__title">&nbsp;</h6>
              <ul>
                <li>
                  <div className="stat-name">FUM</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(bsh.avg_off_fum_lost, 1)}
                  </div>
                </li>
                <li>
                  <div className="stat-name">FP</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(props.player.fppg, 1)}
                  </div>
                </li>
              </ul>
            </div>
          </div>
        );
      }

      // WR/TE
      if (props.player.position === 'WR' || props.player.position === 'TE') {
        return (
          <div className="player-stats">
            <div className="stat-section">
              <h6 className="stats-section__title">Game Avg</h6>
              <ul>
                <li>
                  <div className="stat-name">REC</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(bsh.avg_rec_rec, 1)}
                  </div>
                </li>
                <li>
                  <div className="stat-name">YDS</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(bsh.avg_rush_yds + bsh.avg_rec_yds, 1)}
                  </div>
                </li>
                <li>
                  <div className="stat-name">TD</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(bsh.avg_rush_td + bsh.avg_rec_td, 1)}
                  </div>
                </li>
                <li>
                  <div className="stat-name">FUM</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(bsh.avg_off_fum_lost, 1)}
                  </div>
                </li>
                <li>
                  <div className="stat-name">FP</div>
                  <div className="stat-score">
                    {roundUpToDecimalPlace(props.player.fppg, 1)}
                  </div>
                </li>
              </ul>
            </div>
          </div>
        );
      }

      // Unsupported player position
      return (
        <div className="player-stats"></div>
      );
    }


    case 'nba': {
      return (
        <div className="player-stats">
          <ul>
            <li>
              <div className="stat-name">AVG</div>
              <div className="stat-score">
                {roundUpToDecimalPlace(bsh.avg_fp, 1)}
              </div>
            </li>
            <li>
              <div className="stat-name">PPG</div>
              <div className="stat-score">
                {roundUpToDecimalPlace(bsh.avg_points, 1)}
              </div>
            </li>
            <li>
              <div className="stat-name">RPG</div>
              <div className="stat-score">
                {roundUpToDecimalPlace(bsh.avg_rebounds, 1)}
              </div>
            </li>
            <li>
              <div className="stat-name">APG</div>
              <div className="stat-score">
                {roundUpToDecimalPlace(bsh.avg_assists, 1)}
              </div>
            </li>
            <li>
              <div className="stat-name">STLPG</div>
              <div className="stat-score">
                {roundUpToDecimalPlace(bsh.avg_steals, 1)}
              </div>
            </li>
            <li>
              <div className="stat-name">FPPG</div>
              <div className="stat-score">
                {roundUpToDecimalPlace(props.player.fppg, 1)}
              </div>
            </li>
          </ul>
        </div>
      );
    }


    case 'nhl': {
    // For NHL goalies:
      if (props.player.position === 'G') {
        return (
          <div className="player-stats">
            <ul>
              <li>
                <div className="stat-name">S</div>
                <div className="stat-score">
                  {roundUpToDecimalPlace(bsh.saves, 1)}
                </div>
              </li>
              <li>
                <div className="stat-name">A</div>
                <div className="stat-score">
                  {roundUpToDecimalPlace(bsh.assist, 1)}
                </div>
              </li>
              <li>
                <div className="stat-name">SOG</div>
                <div className="stat-score">
                  {roundUpToDecimalPlace(bsh.sog, 1)}
                </div>
              </li>
              <li>
                <div className="stat-name">FPPG</div>
                <div className="stat-score">
                  {roundUpToDecimalPlace(props.player.fppg, 1)}
                </div>
              </li>
            </ul>
          </div>
        );
      }

      // For regular NHL Players:
      return (
        <div className="player-stats">
          <ul>
            <li>
              <div className="stat-name">G</div>
              <div className="stat-score">
                {roundUpToDecimalPlace(bsh.goal, 1)}
              </div>
            </li>
            <li>
              <div className="stat-name">A</div>
              <div className="stat-score">
                {roundUpToDecimalPlace(bsh.assist, 1)}
              </div>
            </li>
            <li>
              <div className="stat-name">BLK</div>
              <div className="stat-score">
                {roundUpToDecimalPlace(bsh.blk, 1)}
              </div>
            </li>
            <li>
              <div className="stat-name">SOG</div>
              <div className="stat-score">
                {roundUpToDecimalPlace(bsh.sog, 1)}
              </div>
            </li>
            <li>
              <div className="stat-name">FPPG</div>
              <div className="stat-score">
                {roundUpToDecimalPlace(props.player.fppg, 1)}
              </div>
            </li>
          </ul>
        </div>
      );
    }


    default: {
      return (<div className="player-stats"></div>);
    }
  }
};

// Set PropTypes.
DraftPlayerDetailAverages.propTypes = {
  player: React.PropTypes.object.isRequired,
};


module.exports = DraftPlayerDetailAverages;
