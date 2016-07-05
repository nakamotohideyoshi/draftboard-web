import React from 'react';


/**
 * Stateless component that houses MLB pitch within pitch zone
 * - we may want to remove zone at some point, in there right now in case we want to differentiate by them
 *
 * @param  {object} props React props
 * @return {jsx}          JSX of component
 */

export default React.createClass({
  propTypes: {
    decimalRemaining: React.PropTypes.number.isRequired,
    diameter: React.PropTypes.number.isRequired,
  },

  getInitialState() {
    return {
      show: true,
    };
  },

  componentDidMount() {
    this.updateCanvas();
  },

  /**
   * THIS IS A SUPER TERRIBLE HACK
   * Since we have a very complex canvas render with updateCanvas, using 360 rotations,
   * trying to wipe the canvas when the decimalRemaining was a no go. Instead, to force
   * a full rerendering of the canvas, I had to flip a state switch to unrender the canvas,
   * then immediately rerender. Unfortunately this.forceUpdate() doesn't work either,
   * as the canvas tag itself doesn't change.
   * I don't like this, but it does work. Would love a cleaner solution if someone thinks of one.
   */
  componentWillReceiveProps(prevProps) {
    if (prevProps.decimalRemaining !== this.props.decimalRemaining) {
      this.setState({ show: false }, () => this.setState({ show: true }));
    }
  },

  componentDidUpdate(prevProps, prevState) {
    if (prevState !== this.state) this.updateCanvas();
  },

  updateCanvas() {
    const canvas = this.refs.canvas;

    // this gets called when canvas doesn't exist, so just return in these situations
    if (canvas === undefined) return;

    const { diameter, decimalRemaining } = this.props;
    const radiansRemaining = decimalRemaining * 360 - 180;
    const ctx = canvas.getContext('2d');

    // skip update if canvas is not supported (like in tests)
    if (!ctx) return;

    // move to the center
    ctx.translate(diameter / 2, diameter / 2);

    // start the gradient at the point remaining
    ctx.rotate(-radiansRemaining * Math.PI / 180);

    // make sure to cap it so that it's smooth around and the right diameter
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';

    // loop through all 360 degrees and draw a line from the center out
    for (let i = 0; i <= 360; i++) {
      ctx.save();

      // invert the gradient to move from
      ctx.rotate(-Math.PI * i / 180);
      ctx.translate(-ctx.lineWidth / 2, ctx.lineWidth / 2);

      // move to the center
      ctx.beginPath();
      ctx.moveTo(0, 0);

      // top out at 30%, as the comp does
      let percentage = i / 15;
      if (percentage > 40) percentage = 40;

      ctx.strokeStyle = `rgba(0,0,0,${percentage / 100})`;

      // write and close
      ctx.lineTo(0, diameter);
      ctx.stroke();
      ctx.closePath();

      ctx.restore();
    }
  },

  render() {
    if (!this.state.show) return null;

    return (
      <canvas className="live-overall-stats__radial-bg" ref="canvas" width="220" height="220" />
    );
  },
});
