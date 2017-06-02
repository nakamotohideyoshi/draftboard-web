import React from 'react';
import PbpFactory from './PbpFactory';

let pbpQueue;

export default React.createClass({

  propTypes: {
    sport: React.PropTypes.string.isRequired,
    playId: React.PropTypes.string,
    onSportUpdated: React.PropTypes.func.isRequired,
    onPBPUpdated: React.PropTypes.func.isRequired,
  },

  getInitialState() {
    pbpQueue = new PbpFactory(this.props.sport);
    window.pbpQueue = pbpQueue;
    return {
      sport: this.props.sport,
      recaps: pbpQueue.recaps,
    };
  },

  componentWillMount() {
    pbpQueue.onChange = () => {
      if (!pbpQueue.getCurEventObj() || !this.props.onPBPUpdated) {
        return false;
      }
      this.props.onPBPUpdated(pbpQueue.getCurEventObj());
    };

    window.debug_live_animations_which_side = 'mine';
  },

  changePlay() {
    pbpQueue.goto(parseInt(document.getElementById('playMenu').value, 10));
  },

  changeSport() {
    const newSport = document.getElementById('sportMenu').value;

    if (newSport !== this.state.sport) {
      pbpQueue.loadSport(newSport);

      this.setState({
        sport: document.getElementById('sportMenu').value,
        recaps: pbpQueue.getRecaps(),
      });

      this.props.onSportUpdated(newSport);
    }
  },

  changeWhichSide() {
    window.debug_live_animations_which_side = document.getElementById('whichSideMenu').value;
    pbpQueue.replay();
  },

  toggleDebug() {
    window.DEBUG_LIVE_ANIMATIONS = !window.DEBUG_LIVE_ANIMATIONS;
    document.body.classList[window.DEBUG_LIVE_ANIMATIONS ? 'add' : 'remove']('is-debugging');
  },

  renderTimelineForm() {
    const hasPlays = pbpQueue.getRecaps().length > 0;

    if (!hasPlays) {
      return;
    }

    const renderWhichSideMenu = () => (
      <select id="whichSideMenu"
        value={window.debug_live_animations_which_side}
        onChange={() => this.changeWhichSide()}
      >
        <option value="mine">Mine</option>
        <option value="opponent">Opponent</option>
        <option value="both">Both</option>
      </select>
    );

    const renderPlayMenu = (recaps, curIndex) => {
      const playOptions = recaps.map((vo, index) => {
        const label = `${index}. ${vo.playType()} - ${vo.playDescription()}`;
        const isDisabled = vo.playType() === 'unknown_play';
        return (
          <option value={ index } key={ index } disabled={isDisabled}>{ label }</option>
        );
      });

      return (
        <select id="playMenu" value={curIndex} style={{ maxWidth: '300px' }} onChange={() => this.changePlay()}>
          <option value="" disabled>{ hasPlays ? 'Select Play' : 'No Available Plays'}</option>
          { playOptions }
        </select>
      );
    };

    return (
      <div style={{ display: 'inline-block' }}>
        <button onClick={() => pbpQueue.prev()} disabled={!pbpQueue.hasPrev()}>Prev</button>
        <button onClick={() => pbpQueue.next()} disabled={!pbpQueue.hasNext()}>Next</button>
        <button onClick={() => pbpQueue.replay()} disabled={!pbpQueue.getCurEventObj()}>Replay</button>
        { renderPlayMenu(this.state.recaps, pbpQueue.getCurIndex()) }
        { renderWhichSideMenu() }
      </div>
    );
  },

  render() {
    const sportsMenu = (
      <select id="sportMenu" onChange={() => this.changeSport()} value={this.state.sport} readOnly>
        <option value="nba">NBA</option>
        <option value="nfl">NFL</option>
        <option value="nhl">NHL</option>
      </select>
    );

    const debugMenu = (
      <div style={{ display: 'inline-block' }}>
        <input
          onChange={() => this.toggleDebug()}
          id="debug"
          type="checkbox"
          name="debug"
          value="1"
          selected={window.DEBUG_LIVE_ANIMATIONS}
        />
        <label htmlFor="debug">Show Debug</label>
      </div>
    );

    return (
        <div className="debug-menu">
          {sportsMenu}
          {this.renderTimelineForm()}
          {debugMenu}
        </div>
    );
  },
});
