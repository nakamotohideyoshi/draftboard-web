export default class FlightArrow {

  /**
   * Instantiates a Flight Arrow with the start and end points.
   */
  constructor(field, startPt, endPt, arc = 100, startOffsetY = 0, endOffsetY = 0) {
    const startPtWithOffset = {
      x: startPt.x,
      y: startPt.y - startOffsetY,
    };

    const endPtWithOffset = {
      x: endPt.x,
      y: endPt.y - endOffsetY,
    };

    const arrowPoints = this.getPoints(startPtWithOffset, endPtWithOffset);
    const shadowPoints = this.getPoints(startPt, endPt);

    this._progress = 1;
    this._start = startPt;
    this._end = endPt;

    this._maskW = Math.max(arrowPoints.tl.x, arrowPoints.tr.x) - Math.min(arrowPoints.tl.x, arrowPoints.tr.x);
    this._maskX = Math.min(arrowPoints.tl.x, arrowPoints.tr.x);

    this.path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    this.path.setAttribute('d', this.getPath(arrowPoints, arc));
    this.path.setAttribute('style', 'fill:#dedede; fill-opacity:0.75');
    this.path.setAttribute('mask', 'url(#mask)');
    this.path.setAttribute('transform', 'translate(0,0)');

    this.shadow = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    this.shadow.setAttribute('d', this.getPath(shadowPoints, -(arc * 0.5)));
    this.shadow.setAttribute('style', 'fill:#000;fill-opacity:.1;');
    this.shadow.setAttribute('transform', 'translate(-2, 20)');
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

    const x = this._start.x <= this._end.x
      ? offset - this._maskW
      : this._maskW - offset;

    this.maskRect.setAttribute('transform', `translate(${x})`);
  }

  /**
   * Returns an array of x,y pairs describing all points neccessary to
   * create the arrow.
   */
  getPoints(ptA, ptB) {
    const thickness = 4;
    const taper = 1;
    const arcX = ptA.x + (ptB.x - ptA.x) * 0.5;
    const arcY = ptA.y + (ptB.y - ptA.y) * 0.5;

    return {
      // Top left
      tl: { x: ptA.x, y: ptA.y - thickness * 0.5 },
      // Top right
      tr: { x: ptB.x, y: ptB.y - thickness * 0.5 },
      // Top control point
      tcp: { x: arcX, y: arcY - thickness * 0.5 },
      // Bottom right
      br: { x: ptB.x, y: ptB.y + taper * 0.5 },
      // Bottom left
      bl: { x: ptA.x, y: ptA.y + taper * 0.5 },
      // Bottom control point
      bcp: { x: arcX, y: arcY + thickness * 0.5 },
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

    return [
      // Move to the start of the path
      `M${tl.x},${tl.y}`,
      // Control points for top arc
      `Q${tcp.x},${tcp.y - arc} ${tr.x},${tr.y}`,
      // Line to bottom right
      `L${br.x},${br.y}`,
      // Control points for bottom arc
      `Q${bcp.x},${bcp.y - arc} ${bl.x},${bl.y}`,
      // Close the path.
      'Z',
    ].reduce((str, cmd) => ` ${str} ${cmd}`, '');
  }
}
