import React from 'react';
import store from '../../store';
import PbpFactory from './PbpFactory';
import { addEventAndStartQueue } from '../../actions/events';

const pbpQueue = new PbpFactory();

export default React.createClass({
  componentWillMount() {
    pbpQueue.onChange = () => {
      const gameId = 3;
      const gameEvent = pbpQueue.getCurEventObj();
      const eventType = 'pbp';
      const sport = 'nba';
      store.dispatch(addEventAndStartQueue(gameId, gameEvent, eventType, sport));
    };
  },

  changeLineup() {
    pbpQueue.setWhichSide(document.getElementById('lineupMenu').value);
  },

  changePlay() {
    pbpQueue.goto(parseInt(document.getElementById('playMenu').value, 10));
  },

  toggleDebug() {
    window.DEBUG_LIVE_ANIMATIONS = !window.DEBUG_LIVE_ANIMATIONS;
    document.body.classList[window.DEBUG_LIVE_ANIMATIONS ? 'add' : 'remove']('is-debugging');
  },

  render() {
    const playOptions = pbpQueue.recaps
      .map((vo, index) => {
        const label = `${vo.playType()} - ${vo.madeShot()} - ${vo._obj.description}`;
        return (
          <option value={ index } key={ vo._obj.id }>{ label }</option>
        );
      }
    );

    return (
        <div className="debug-menu">
          <button onClick={ () => pbpQueue.prev() } disabled={!pbpQueue.hasPrev()}>Prev</button>
          <button onClick={ () => pbpQueue.next() } disabled={!pbpQueue.hasNext()}>Next</button>
          <button onClick={ () => pbpQueue.replay() } disabled={!pbpQueue.getCurEventObj()}>Replay</button>
          <select id="playMenu" value={ pbpQueue.getCurIndex() } onChange={ () => this.changePlay() } >
            <option value="" disabled>Select Play</option>
            { playOptions }
          </select>
          <select id="lineupMenu" onChange={ () => this.changeLineup() }>
            <option value="mine">Mine</option>
            <option value="both">Both</option>
            <option value="opponent">Opponent</option>
          </select>
          <select id="sportMenu" value="nba" readOnly>
            <option value="nba">NBA</option>
            <option value="nfl" disabled>NFL</option>
            <option value="nhl" disabled>NHL</option>
          </select>
          <input
            onChange={() => this.toggleDebug()}
            id="debug"
            type="checkbox"
            name="debug"
            value="1"
            selected={window.DEBUG_LIVE_ANIMATIONS}
          /><label htmlFor="debug">Show Debug</label>
        </div>
      );
  },
});
