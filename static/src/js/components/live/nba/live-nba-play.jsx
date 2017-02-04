import PlayAnimation from '../../../lib/live-animations/nba/PlayAnimation';
import NBACourt from '../../../lib/live-animations/nba/NBACourt';
import NBAPlayRecapVO from '../../../lib/live-animations/nba/NBAPlayRecapVO';
import React from 'react';
import Raven from 'raven-js';

require('../../../../sass/blocks/live/nba/live-nba-play.scss');

export default React.createClass({
  propTypes: {
    event: React.PropTypes.object.isRequired,
    animationCompleted: React.PropTypes.func,
    animationStarted: React.PropTypes.func,
  },

  componentDidMount() {
    const court = new NBACourt(this.refs.dom);
    const recap = new NBAPlayRecapVO(this.props.event);
    const animation = new PlayAnimation();

    this.animationStarted();

    animation.play(recap, court).catch(error =>
      Raven.captureMessage('Live animation failed', { extra: { error, event } })
    ).then(
      () => this.animationCompleted()
    ).catch(
      // ESLint forced catch (catch-or-return).
    );
  },

  animationStarted() {
    if (this.props.animationStarted) {
      this.props.animationStarted();
    }
  },

  animationCompleted() {
    if (this.props.animationCompleted) {
      this.props.animationCompleted();
    }
  },

  render() {
    return <span className="live-nba-court__live-nba-play" ref="dom"></span>;
  },
});
