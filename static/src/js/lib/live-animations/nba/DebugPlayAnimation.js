import LiveAnimation from '../LiveAnimation';
import NBAPlayRecapVO from './NBAPlayRecapVO';

export default class DebugPlayAnimation extends LiveAnimation {

  /**
   * Draws a rectangle.
   */
  drawRect(x, y, w, h, style = 'fill:#bdcc1a;') {
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', x);
    rect.setAttribute('y', y);
    rect.setAttribute('width', w);
    rect.setAttribute('height', h);
    rect.setAttribute('style', style);
    this.svg.appendChild(rect);
    return rect;
  }

  /**
   * Draws a polygon.
   */
  drawPoly(points, style = 'fill:#bdcc1a;') {
    const start = points[0];
    const path = points.reduce((str, pt) => `${str} L${pt.x},${pt.y}`, `M${start.x},${start.y}`);
    const poly = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    poly.setAttribute('d', `${path} Z`);
    poly.setAttribute('style', style);
    this.svg.appendChild(poly);
    return poly;
  }

  /**
   * Draws a circle.
   */
  drawCircle(x, y, style = 'fill:#bdcc1a;', radius = 2) {
    const circ = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circ.setAttribute('r', radius);
    circ.setAttribute('cx', x);
    circ.setAttribute('cy', y);
    circ.setAttribute('style', style);
    this.svg.appendChild(circ);
    return circ;
  }

  /**
   * Draws a rectangle outlining the court's dimensions.
   */
  drawCourtRect(court) {
     // Court rect.
    const tl = court.getPosition(0, 0);
    const tr = court.getPosition(1, 0);
    const br = court.getPosition(1, 1);
    const bl = court.getPosition(0, 1);
    return this.drawPoly([tl, tr, br, bl], 'fill:#00ff00; fill-opacity:0.2');
  }

  /**
   * Draws a polygon for each of the court's zones.
   */
  drawZones(court, recap) {
    court.getZones().forEach((zone, index) => {
      const positions = zone.map(pos => {
        const loc = pos;
        if (recap.teamBasket() === NBAPlayRecapVO.BASKET_RIGHT) {
          loc.x = 1 - loc.x;
        }

        return court.getPosition(loc.x, loc.y);
      });

      const inZone = court.getZoneAtPosition(recap.courtPosition(), recap.teamBasket()) === index;
      const opacity = inZone ? 0.5 : [0.1, 0.2][index % 2];

      return this.drawPoly(positions, `fill:#000000; fill-opacity:${opacity};`);
    });
  }

  /**
   * Draws a circle at the court's basket position.
   */
  drawBasketMarker(court, recap) {
    const basketPos = court.getBasketPos(recap.teamBasket());
    const basketMarkerPos = court.getPosition(basketPos.x, basketPos.y);
    return this.drawCircle(basketMarkerPos.x, basketMarkerPos.y, 'fill:#FF0000; fill-opacity:0.65', 3);
  }

  /**
   * Draws a circle at the court's rim position.
   */
  drawRimMarker(court, recap) {
    const rimPos = court.getRimPos(recap.teamBasket());
    const rimMarkerPos = court.getPosition(rimPos.x, rimPos.y);
    return this.drawCircle(rimMarkerPos.x, rimMarkerPos.y, 'fill:#FF00FF; fill-opacity:0.65', 3);
  }

  /**
   * Draws a line from the basket to a circle indicating the play's
   * court position.
   */
  drawPlayerMarker(court, recap) {
    if (recap.playType() === NBAPlayRecapVO.DUNK ||
        recap.playType() === NBAPlayRecapVO.FREETHROW ||
        recap.playType() === NBAPlayRecapVO.LAYUP ||
        recap.playType() === NBAPlayRecapVO.REBOUND
    ) {
      return;
    }

    const basketPos = court.getBasketPos(recap.teamBasket());
    const basketMarkerPos = court.getPosition(basketPos.x, basketPos.y);
    const { x: playerX, y: playerY } = recap.courtPosition();
    const playerPos = court.getPosition(playerX, playerY);

    // Player Angle
    const styles = 'stroke:#FF0000; stroke-width:1; stroke-opacity:.25;';
    this.drawPoly([basketMarkerPos, playerPos, basketMarkerPos], styles);
    return this.drawCircle(playerPos.x, playerPos.y, 'fill:#00FF00; fill-opacity:0.85', 2);
  }

  play(recap, court) {
    this.svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    this.svg.setAttribute('width', court.getWidth());
    this.svg.setAttribute('height', court.getHeight());
    this.svg.style.display = 'block';
    court.addChild(this.svg);

    this.drawCourtRect(court);
    this.drawZones(court, recap);
    this.drawBasketMarker(court, recap);
    this.drawRimMarker(court, recap);
    this.drawPlayerMarker(court, recap);

    return super.play(recap, court);
  }
}
