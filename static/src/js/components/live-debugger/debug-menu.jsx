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
      debugLayout: window.DEBUG_LIVE_ANIMATIONS_LAYOUT,
      debugClips: window.DEBUG_LIVE_ANIMATIONS_CLIPS,
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

  toggleDebugLayout() {
    window.DEBUG_LIVE_ANIMATIONS_LAYOUT = !window.DEBUG_LIVE_ANIMATIONS_LAYOUT;
    this.setState({ debugLayout: window.DEBUG_LIVE_ANIMATIONS_LAYOUT });
    document.body.classList[window.DEBUG_LIVE_ANIMATIONS_LAYOUT ? 'add' : 'remove']('is-debugging');
  },

  toggleDebugClips() {
    window.DEBUG_LIVE_ANIMATIONS_CLIPS = !window.DEBUG_LIVE_ANIMATIONS_CLIPS;
    this.setState({ debugClips: window.DEBUG_LIVE_ANIMATIONS_CLIPS });
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
      <div style={{ display: 'inline-block', paddingLeft: '20px' }}>
        <span>Debug </span>
        <div style={{ display: 'inline-block' }}>
          <input
            onChange={() => this.toggleDebugClips()}
            id="debug-clips"
            type="checkbox"
            name="debug-clips"
            value="1"
            checked={this.state.debugClips}
          />
          <label htmlFor="debug-clips"> Clips&nbsp;</label>
        </div>
        <div style={{ display: 'inline-block' }}>
          <input
            onChange={() => this.toggleDebugLayout()}
            id="debug-layout"
            type="checkbox"
            name="debug-layout"
            value="1"
            checked={this.state.debugLayout}
          />
          <label htmlFor="debug-layout"> Layout&nbsp;</label>
        </div>
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
