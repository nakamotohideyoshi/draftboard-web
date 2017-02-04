import React from 'react';
import LiveAnimationArea from '../live/live-animation-area';
import LiveBigPlays from '../live/live-big-plays';
import PbpFactory from './PbpFactory';

const pbpQueue = new PbpFactory();

export default React.createClass({

  getInitialState() {
    return {
      pbp: pbpQueue.getCurEventObj(),
      queue: [pbpQueue.getCurEventObj()],
    };
  },

  componentWillMount() {
    pbpQueue.onChange = () => {
      const pbp = pbpQueue.getCurEventObj();
      const queue = this.state.queue.concat([pbp]);

      this.setState({ pbp, queue });
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

  renderDebugMenu() {
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
        const isDisabled = vo.playType() === 'unknown_play' ? 'disabed' : '';
        const label = `${vo.playType()} - ${vo._obj.description}`;
        return (
          <option disabled={ isDisabled } value={ index } key={ vo._obj.id }>{ label }</option>
        );
      }
    );

    return (
        <div style={ styles }>
          <button onClick={ () => pbpQueue.next() }>Next</button>
          <button onClick={ () => pbpQueue.prev() }>Prev</button>
          <button onClick={ () => pbpQueue.replay() }>Replay</button>
          <select id="playMenu" value={ pbpQueue.getCurIndex() } onChange={ () => this.changePlay() } >
            { playOptions }
          </select>
          <select id="lineupMenu" onChange={ () => this.changeLineup() }>
            <option value="mine">Mine</option>
            <option value="both">Both</option>
            <option value="opponent">Opponent</option>
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

  render() {
    return (
      <section className="debug-live-animations">
        { this.renderDebugMenu() }
        <div className="live">
          <section className="live__venues">
            <div className="live__venues-inner">
              <LiveAnimationArea watching={ { sport: 'nba' } } animationEvent={ this.state.pbp } eventsMultipart={{}} />
            </div>
          </section>
          <LiveBigPlays queue={this.state.queue} />
        </div>
      </section>
    );
  },
});
