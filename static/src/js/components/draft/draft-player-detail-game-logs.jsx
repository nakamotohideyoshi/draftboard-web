import React from 'react';
import moment from 'moment';
import log from '../../lib/logging';

/**
 * Render a list of <th> headers from the provided column array.
 * @param  {[type]} cols [description]
 * @return {[type]}      [description]
 */
const renderHeaders = (cols) => cols.map((col, i) => <th key={i}>{col}</th>);


/**
 * Show a player's season averages (or is it last 10 game averages?). This sits
 * directly below the player images on the player detail panel in the draft
 * section.
 */
const DraftPlayerDetailGameLogs = (props) => {
  // If there is no boxscore history
  if (
    'splitsHistory' in props.player
    && !Object.keys(props.player.splitsHistory).length
  ) {
    return (<div className="player-stats">No Game Logs</div>);
  }

  switch (props.player.sport) {
    /**
     * NFL
     */
    case 'nfl': {
      // QB
      if (props.player.position === 'QB') {
        const gameLogs = props.player.splitsHistory.map((game, index) => (
          <tr key={index}>
            <td key="1">{game.opp}</td>
            <td key="2">{moment.utc(game.date).format('M/D/YY')}</td>
            <td key="3">{game.pass_yds}</td>
            <td key="4">{game.pass_td}</td>
            <td key="5">{game.pass_int}</td>
            <td key="6">{game.rush_yds}</td>
            <td key="7">{game.rush_td}</td>
            <td key="10">{game.off_fum_lost}</td>
            <td key="11">{game.fp}</td>
          </tr>
        ));

        return (
          <div className="player-splits">
            <table className="table">
              <thead className="header">
                <tr>
                  <th colSpan="2"></th>
                  <th colSpan="3">Passing</th>
                  <th colSpan="2">Rushing</th>
                  <th colSpan="2"></th>
                </tr>
                <tr>
                  {renderHeaders(
                    ['opp', 'date', 'yds', 'td', 'int', 'yds', 'td', 'fum', 'fp']
                  )}
                </tr>
              </thead>
              <tbody>
                {gameLogs}
              </tbody>
            </table>
          </div>
        );
      }

      // RB, WR, TE, FB
      if (['RB', 'WR', 'TE', 'FB'].includes(props.player.position)) {
        const gameLogs = props.player.splitsHistory.map((game, index) => (
          <tr key={index}>
            <td key="1">{game.opp}</td>
            <td key="2">{moment.utc(game.date).format('M/D/YY')}</td>
            <td key="6">{game.rush_yds}</td>
            <td key="7">{game.rush_td}</td>
            <td key="4">{game.rec_yds}</td>
            <td key="5">{game.rec_td}</td>
            <td key="10">{game.off_fum_lost}</td>
            <td key="11">{game.fp}</td>
          </tr>
        ));

        return (
          <div className="player-splits">
            <table className="table">
              <thead className="header">
                <tr>
                  <th colSpan="2"></th>
                  <th colSpan="2">Rushing</th>
                  <th colSpan="2">Receiving</th>
                  <th colSpan="2"></th>
                </tr>
                <tr>
                  {renderHeaders(
                    ['opp', 'date', 'yds', 'td', 'yds', 'td', 'fum', 'fp']
                  )}
                </tr>
              </thead>
              <tbody>
                {gameLogs}
              </tbody>
            </table>
          </div>
        );
      }

      log.warn(`Unsupported player position: ${props.player.position}`);

      // Unsupported player position
      return (<div></div>);
    }


    case 'nba': {
      const gameLogs = props.player.splitsHistory.map((game, index) => (
        <tr key={index}>
          <td key="1">{game.opp}</td>
          <td key="2">{moment.utc(game.date).format('M/D/YY')}</td>
          <td key="6">{game.points}</td>
          <td key="7">{game.rebounds}</td>
          <td key="4">{game.assists}</td>
          <td key="10">{game.blocks}</td>
          <td key="5">{game.steals}</td>
          <td key="11">{game.minutes}</td>
          <td key="12">{game.turnovers}</td>
          <td key="13">{game.fp}</td>
        </tr>
      ));

      return (
        <div className="player-splits">
          <table className="table">
            <thead className="header">
              <tr>
                {renderHeaders(
                  ['opp', 'date', 'pts', 'reb', 'ast', 'blk', 'stl', 'min', 'to', 'fp']
                )}
              </tr>
            </thead>
            <tbody>
              {gameLogs}
            </tbody>
          </table>
        </div>
      );
    }


    case 'nhl': {
    // For NHL goalies:
      if (props.player.position === 'G') {
        return (<div></div>);
      }

      // For regular NHL Players:
      const gameLogs = props.player.splitsHistory.map((game, index) => (
        <tr key={index}>
          <td key="1">{game.opp}</td>
          <td key="2">{moment.utc(game.date).format('M/D/YY')}</td>
          <td key="6">{game.goal}</td>
          <td key="7">{game.assist}</td>
          <td key="4">{game.blocks}</td>
          <td key="10">{game.sog}</td>
          <td key="5">{game.saves}</td>
          <td key="11">{game.ga}</td>
          <td key="11">{game.fp}</td>
        </tr>
      ));

      return (
        <div className="player-splits">
          <table className="table">
            <thead className="header">
              <tr>
                {renderHeaders(
                  ['opp', 'date', 'g', 'ast', 'blk', 'sog', 's', 'ga', 'fp']
                )}
              </tr>
            </thead>
            <tbody>
              {gameLogs}
            </tbody>
          </table>
        </div>
      );
    }


    default: {
      return (<div></div>);
    }
  }
};

// Set PropTypes.
DraftPlayerDetailGameLogs.propTypes = {
  player: React.PropTypes.object.isRequired,
};


module.exports = DraftPlayerDetailGameLogs;
