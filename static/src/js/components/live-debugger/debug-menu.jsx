import React from 'react';
import store from '../../store';
import PbpFactory from './PbpFactory';

const pbpQueue = new PbpFactory();

export default React.createClass({
  componentWillMount() {
    pbpQueue.onChange = () => {
      store.dispatch({
        type: 'EVENT__SET_CURRENT',
        value: pbpQueue.getCurEventObj(),
      });
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
  },

  render() {
    const styles = {
      position: 'fixed',
      top: 0,
      left: 0,
      zIndex: 999,
      width: '100%',
      padding: '20px',
      backgroundColor: '#000',
      color: '#fff',
    };

    const playOptions = pbpQueue.recaps
      .map((vo, index) => {
        const label = `${vo.playType()} - ${vo._obj.description}`;
        return (
          <option value={ index } key={ vo._obj.id }>{ label }</option>
        );
      }
    );

    return (
        <div style={ styles }>
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
