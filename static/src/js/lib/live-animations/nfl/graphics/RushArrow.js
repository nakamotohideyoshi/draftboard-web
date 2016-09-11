export default class RushArrow {

  constructor(field, startingYardLine, endingYardLine, yardLineY = 0.5, color = '#dedede', opacity = 0.75) {
    this._progress = 1;

    this.field = field;
    this.startingYardLine = startingYardLine;
    this.endingYardLine = endingYardLine;
    this.yardLineY = yardLineY;

    const points = this.getPoints(field, startingYardLine, endingYardLine, yardLineY);

    this.arrow = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    this.arrow.setAttribute('d', this.getPath(points));
    this.arrow.setAttribute('style', `fill:${color};fill-opacity:${opacity}`);

    this.shadow = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    this.shadow.setAttribute('d', this.getPath(points));
    this.shadow.setAttribute('style', 'fill:#000;fill-opacity:.20;');
    this.shadow.setAttribute('transform', 'translate(-2,6)');

    this.el = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    this.el.setAttribute('width', field.getWidth());
    this.el.setAttribute('height', field.getHeight());
    this.el.style.display = 'block';
    this.el.appendChild(this.shadow);
    this.el.appendChild(this.arrow);
  }

  /**
   * Returns the progress of the arrow.
   * @return {number} The progress.
   */
  get progress() {
    return this._progress;
  }

  /**
   * Set the progress of the arrow 0 - 1.
   * @param {number} The new progress.
   */
  set progress(value) {
    const points = this.getPoints(this.field, this.startingYardLine, this.endingYardLine, this.yardLineY);
    const path = this.getPath(points);
    this._progress = Math.max(0, Math.min(1, value));
    this.shadow.setAttribute('d', path);
    this.arrow.setAttribute('d', path);
  }

  /**
   * Returns an array of x,y pairs describing the path of the arrow.
   * @param {NFLField}
   * @param {Float}
   * @param {Float}
   * @param {Float}
   * @return {Array}
   */
  getPoints(field, startingYardLine, endingYardLine, yardLineY) {
    // The height of the bar
    const barThickness = 0.04;
    // The height of the tip
    const tipThickness = 0.06;
    // The width is 2 yards wide.
    const tipWidth = (startingYardLine > endingYardLine) ? -0.02 : 0.02;
    // The Y axis of the top of the bar.
    const barTop = yardLineY - barThickness * 0.5;
    // The Y axis of the bottom of the bar.
    const barBottom = yardLineY + barThickness * 0.5;
    // The length of the bar in yards.
    const len = Math.max(endingYardLine, startingYardLine) - Math.min(endingYardLine, startingYardLine);

    // The end of the bar is the startingYardLine minus/plus the width
    // of the tip and length of the bar.
    const barEnd = startingYardLine > endingYardLine
      ? startingYardLine - (len - Math.abs(tipWidth)) * this._progress
      : startingYardLine + (len - Math.abs(tipWidth)) * this._progress;

    // Describe the tip of the arrows coordinates.
    const tipTop = barTop - tipThickness * 0.5;
    const tipPointX = barEnd + tipWidth;
    const tipBottom = barBottom + tipThickness * 0.5;

    return {
      bar: {
        tl: field.getFieldPos(startingYardLine, barTop),
        tr: field.getFieldPos(barEnd, barTop),
        br: field.getFieldPos(barEnd, barBottom),
        bl: field.getFieldPos(startingYardLine, barBottom),
      },
      tip: {
        top: field.getFieldPos(barEnd, tipTop),
        point: field.getFieldPos(tipPointX, yardLineY),
        bottom: field.getFieldPos(barEnd, tipBottom),
      },
    };
  }

  /**
   * Returns the path instructions for the rush arrow.
   */
  getPath(points) {
    const { bar, tip } = points;

    return [
      // Move to the start of the path
      `M${bar.tl.x},${bar.tl.y}`,
      // Line to the top right of the bar
      `L${bar.tr.x},${bar.tr.y}`,
      // Line to the top of the tip
      `L${tip.top.x},${tip.top.y}`,
      // Line to the center of the tip - point
      `L${tip.point.x},${tip.point.y}`,
      // Line to the bottom of the tip
      `L${tip.bottom.x},${tip.bottom.y}`,
      // Line to the bottom right of the bar
      `L${bar.br.x},${bar.br.y}`,
      // Line to the bottom left of the bar
      `L${bar.bl.x},${bar.bl.y}`,
      // Close the path
      'Z',
    ].reduce((str, cmd) => ` ${str} ${cmd}`, '');
  }
}
