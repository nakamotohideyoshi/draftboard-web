export default class Rectangle {
  constructor(field, x, y, width, height, color = '#00FF00') {
    const points = this.getPoints(field, x, y, width, height);

    this.marker = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    this.marker.setAttribute('d', this.describeRect(points));
    this.marker.setAttribute('style', `fill:${color}; fill-opacity:0.65`);

    this.el = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    this.el.setAttribute('width', field.getWidth());
    this.el.setAttribute('height', field.getHeight());
    this.el.style.display = 'block';
    this.el.appendChild(this.marker);
  }

  /**
   * Returns the points used for drawing the marker.
   */
  getPoints(field, x, y, w, h) {
    return {
      tl: field.getFieldPos(x, y),
      tr: field.getFieldPos(x + w, y),
      br: field.getFieldPos(x + w, y + h),
      bl: field.getFieldPos(x, y + h),
    };
  }

  /**
   * Returns the path instructions for the marker.
   */
  describeRect(points) {
    const { tl, tr, br, bl } = points;

    return [
      // Move to the start of the path
      `M${tl.x},${tl.y}`,
      // Line to the top right
      `L${tr.x},${tr.y}`,
      // Line to bottom right
      `L${br.x},${br.y}`,
      // Control point for bottom arc
      `L${bl.x},${bl.y}`,
      // Close the path.
      'Z',
    ].reduce((str, cmd) => ` ${str} ${cmd}`, '');
  }
}
