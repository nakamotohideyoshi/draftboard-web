export default class FlightArrow {

  constructor(field, startingYardLine, endingYardLine, startYardLineY, endYardLineY, arc = 100) {
    const points = this.getPoints(field, startingYardLine, endingYardLine, startYardLineY, endYardLineY);

    this._progress = 1;
    this._startingYardLine = startingYardLine;
    this._endingYardLine = endingYardLine;
    this._maskW = Math.max(points.tl.x, points.tr.x) - Math.min(points.tl.x, points.tr.x);
    this._maskX = Math.min(points.tl.x, points.tr.x);

    this.path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    this.path.setAttribute('d', this.getPath(points, arc));
    this.path.setAttribute('style', 'fill:#dedede; fill-opacity:0.75');
    this.path.setAttribute('transform', 'translate(0,-28)');
    this.path.setAttribute('mask', 'url(#mask)');

    this.shadow = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    this.shadow.setAttribute('d', this.getPath(points, -(arc * 0.5)));
    this.shadow.setAttribute('style', 'fill:#000;fill-opacity:.2;');
    this.shadow.setAttribute('transform', 'translate(-2,0)');
    this.shadow.setAttribute('mask', 'url(#mask)');

    this.maskRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    this.maskRect.setAttribute('x', this._maskX);
    this.maskRect.setAttribute('y', 0);
    this.maskRect.setAttribute('width', this._maskW);
    this.maskRect.setAttribute('height', field.getHeight());
    this.maskRect.setAttribute('fill', '#FFFFFF');

    this.defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    this.mask = document.createElementNS('http://www.w3.org/2000/svg', 'mask');
    this.mask.setAttribute('id', 'mask');
    this.mask.appendChild(this.maskRect);
    this.defs.appendChild(this.mask);

    this.el = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    this.el.setAttribute('width', field.getWidth());
    this.el.setAttribute('height', field.getHeight());
    this.el.style.display = 'block';
    this.el.appendChild(this.defs);
    this.el.appendChild(this.shadow);
    this.el.appendChild(this.path);
  }

  /**
   * Returns the progress of the arrow.
   */
  get progress() {
    return this._progress;
  }

  /**
   * Set the progress of the arrow 0 - 1.
   */
  set progress(value) {
    this._progress = Math.max(0, Math.min(1, value));

    const offset = this._progress * this._maskW;

    const x = this._startingYardLine <= this._endingYardLine
      ? offset - this._maskW
      : this._maskW - offset;

    this.maskRect.setAttribute('transform', `translate(${x})`);
  }

  /**
   * Returns an array of x,y pairs describing all points neccessary to
   * create the arrow.
   */
  getPoints(field, startingYardLine, endingYardLine, startYardLineY, endYardLineY) {
    const thickness = 0.08;
    const startY = startYardLineY;
    const endY = endYardLineY;

    const arcX = startingYardLine + (endingYardLine - startingYardLine) * 0.5;
    const arcY = startY + (endY - startY) * 0.5;

    return {
      // Top left
      tl: field.getFieldPos(startingYardLine, startY - thickness * 0.1),
      // Top right
      tr: field.getFieldPos(endingYardLine, endY - thickness * 0.1),
      // Top control point
      tcp: field.getFieldPos(arcX, arcY - thickness * 0.5),
      // Bottom right
      br: field.getFieldPos(endingYardLine, endY + thickness * 0.1),
      // Bottom left
      bl: field.getFieldPos(startingYardLine, startY + thickness * 0.1),
      // Bottom control point
      bcp: field.getFieldPos(arcX, arcY + thickness * 0.5),
    };
  }

  /**
   * Returns the path instructions for the pass arrow arc.
   */
  getPath(points, arc = 200) {
    const { tl, tr, tcp, br, bcp, bl } = points;

    // The lower arc has an %8 percent increase on Y to visually
    // balance the top and bottom arcs by moving them closer together.
    // This number is subjective and was chosen by trial and error.
    const lowerArc = arc + (arc * 0.02);

    return [
      // Move to the start of the path
      `M${tl.x},${tl.y}`,
      // Control point for top arc
      `Q${tcp.x},${tcp.y - arc} ${tr.x},${tr.y}`,
      // Line to bottom right
      `L${br.x},${br.y}`,
      // Control point for bottom arc
      `Q${bcp.x},${bcp.y - lowerArc} ${bl.x},${bl.y}`,
      // Close the path.
      'Z',
    ].reduce((str, cmd) => ` ${str} ${cmd}`, '');
  }
}
