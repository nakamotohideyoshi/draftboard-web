import Stage from '../Stage';

export default class NBACourt extends Stage {

  static get DEFAULT_ZONE() {
    return 2;
  }

  /**
   * Returns the pixel coordinates of the trapazoidal field of play.
   * @return {Object} Four corners of the stage.
   */
  getRect() {
    return {
      topLeft: { x: 245, y: 30 },
      topRight: { x: 1034, y: 30 },
      bottomLeft: { x: 63, y: 217 },
      bottomRight: { x: 1217, y: 217 },
    };
  }

  /**
   * Returns the court position of the basket.
   * @return {Object} Point representing the position of the basket.
   */
  getBasketPos(side = 'left') {
    const basketX = side === 'left' ? 0 : 1;
    return { x: basketX, y: 0.4 };
  }

  /**
   *
   */
  getRimPos(side = 'left') {
    const rimX = side === 'left' ? -0.014 : 1 - (-0.014);
    return { x: rimX, y: 0.03 };
  }

  /**
   * Returns the courts free throw position.
   */
  getFreethrowPos(side = 'left') {
    const freeThrowX = side === 'left' ? 0.21 : 1 - 0.21;
    return { x: freeThrowX, y: this.getBasketPos(side).y };
  }

  /**
   * Returns an array of zone shapes.
   * @return {Array} An array of polygons representing each zone.
   */
  getZones() {
    return [
      [this.getBasketPos(), { x: 0.18, y: 1.0 }, { x: 0.00, y: 1.0 }], // Zone 1
      [this.getBasketPos(), { x: 0.18, y: 1.0 }, { x: 0.50, y: 1.0 }], // Zone 2
      [this.getBasketPos(), { x: 0.50, y: 0.0 }, { x: 0.50, y: 1.0 }], // Zone 3
      [this.getBasketPos(), { x: 0.18, y: 0.0 }, { x: 0.50, y: 0.0 }], // Zone 4
      [this.getBasketPos(), { x: 0.00, y: 0.0 }, { x: 0.18, y: 0.0 }], // Zone 5
    ];
  }

  /**
   * Helper method for determining if the provided x,y coordinate is
   * located inside an array of points.
   * https://github.com/substack/point-in-polygon
   * @param {Object} The survey position.
   * @param {Array} Array of points defining the polygon.
   */
  isPositionInsideZone({ x, y }, zone) {
    let isInside = false;

    for (let i = 0, j = zone.length - 1; i < zone.length; j = i++) {
      const xi = zone[i].x;
      const yi = zone[i].y;
      const xj = zone[j].x;
      const yj = zone[j].y;

      const intersect = ((yi > y) !== (yj > y))
          && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);

      if (intersect) isInside = !isInside;
    }

    return isInside;
  }

  /**
   * Returns the zone for the provided x,y position.
   * @param {Object} The survey position.
   * @param {String} The side of the court to reference.
   * @return {Number} The index of the encompassing zone.
   */
  getZoneAtPosition({ x, y }, side = 'left') {
    const pos = { x, y };

    const zones = this.getZones();

    // If the target basket is on the right side of the court,
    // normalize the x position into the court's zones which are only
    // defined on the left side of the court.

    if (side === 'right') {
      pos.x = 1 - pos.x;
    }

    for (let i = 0; i < zones.length; i++) {
      if (this.isPositionInsideZone(pos, zones[i])) {
        return i;
      }
    }

    return NBACourt.DEFAULT_ZONE;
  }
}
