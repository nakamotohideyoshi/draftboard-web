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

    const arrowPoints = this.getPoints(field, startPtWithOffset, endPtWithOffset);
    const shadowPoints = this.getPoints(field, startPt, endPt);

    this._progress = 1;
    this._start = startPt;
    this._end = endPt;

    this._maskW = Math.max(arrowPoints.tl.x, arrowPoints.tr.x) - Math.min(arrowPoints.tl.x, arrowPoints.tr.x);
    this._maskX = Math.min(arrowPoints.tl.x, arrowPoints.tr.x);

    this.path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    this.path.setAttribute('d', this.getPath(arrowPoints, arc));
    this.path.setAttribute('style', 'fill:#dedede; fill-opacity:0.75');
    this.path.setAttribute('mask', 'url(#mask)');
    this.path.setAttribute('transform', 'translate(0, -25)');

    this.shadow = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    this.shadow.setAttribute('d', this.getPath(shadowPoints, -(arc * 0.5)));
    this.shadow.setAttribute('style', 'fill:#000;fill-opacity:.1;');
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

    const x = this._start.x <= this._end.x
      ? offset - this._maskW
      : this._maskW - offset;

    this.maskRect.setAttribute('transform', `translate(${x})`);
  }

  /**
   * Returns an array of x,y pairs describing all points neccessary to
   * create the arrow.
   */
  getPoints(field, ptA, ptB) {
    const thickness = 0.08;
    const taper = thickness * 0.1;
    const arcX = ptA.x + (ptB.x - ptA.x) * 0.5;
    const arcY = ptA.y + (ptB.y - ptA.y) * 0.5;

    return {
      // Top left
      tl: field.getFieldPos(ptA.x, ptA.y - taper),
      // Top right
      tr: field.getFieldPos(ptB.x, ptB.y - taper),
      // Top control point
      tcp: field.getFieldPos(arcX, arcY - thickness * 0.5),
      // Bottom right
      br: field.getFieldPos(ptB.x, ptB.y + taper),
      // Bottom left
      bl: field.getFieldPos(ptA.x, ptA.y + taper),
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
    const lowerArc = arc; // + (arc * 0.02);

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
