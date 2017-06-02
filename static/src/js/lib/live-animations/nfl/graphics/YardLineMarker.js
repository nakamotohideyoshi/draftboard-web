export default class YardLineMarker {
  constructor(field, yardLine, color = '#bdcc1a') {
    const points = this.getPoints(field, yardLine);

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
  getPoints(field, yardLine) {
    // Determine the left and right position of the line based on
    // the width of the line. The width of the line is hardcoded
    // to approximately match the onfield graphics.
    const lineWidth = 0.003;
    const lineLeft = yardLine - lineWidth;
    const lineRight = lineLeft + lineWidth;

    return {
      tl: field.getFieldPos(lineLeft, 0),
      tr: field.getFieldPos(lineRight, 0),
      br: field.getFieldPos(lineRight, 1),
      bl: field.getFieldPos(lineLeft, 1),
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
