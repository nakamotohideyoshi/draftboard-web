import LiveAnimation from './LiveAnimation';
import { createPath, createSVGElement } from './svgTools';
import NFLPlayRecapVO from './NFLPlayRecapVO';

export default class RushArrowAnimation extends LiveAnimation {

  /**
   * Returns an SVG arrow based on the provided field and
   * starting/ending yard lines.
   */
  createArrow(field, startingYardLine, endingYardLine, color = '#dedede', opacity = 0.75) {
    const barStart = startingYardLine;
    let barEnd = endingYardLine;
    const barTop = 0.38;
    const barBottom = 0.42;

    const tipWidth = 0.02;
    const tipHeight = 0.04;
    const tipTop = barTop - tipHeight;
    const tipPointY = 0.40;
    const tipPointX = barEnd;
    const tipBottom = barBottom + tipHeight;

    // Substract or add the width of the tip to the end
    // of the bar based on the arrows direction.
    if (barStart > barEnd) {
      barEnd += tipWidth;
    } else {
      barEnd -= tipWidth;
    }

    const points = [
      field.getFieldPos(barStart, barTop),
      field.getFieldPos(barEnd, barTop),
      // Begin tip of arrow
      field.getFieldPos(barEnd, tipTop),
      field.getFieldPos(tipPointX, tipPointY),
      field.getFieldPos(barEnd, tipBottom),
      // End tip of arrow
      field.getFieldPos(barEnd, barBottom),
      field.getFieldPos(barStart, barBottom),
    ].map(pt => [pt.x, pt.y]);

    const arrow = createPath(points);
    arrow.setAttribute('style', `fill:${color};fill-opacity:${opacity}`);

    const shadow = createPath(points);
    shadow.setAttribute('style', 'fill:#000;fill-opacity:.25;');
    shadow.setAttribute('transform', 'translate(-2,6)');

    const svg = createSVGElement(field.getWidth(), field.getHeight());
    svg.style.display = 'block';
    svg.appendChild(shadow);
    svg.appendChild(arrow);

    return svg;
  }

  /**
   * Returns the starting line of the rush.
   * @return {number}
   */
  getRushStartingYardLine(recap) {
    // Define a slight offset to help move the arrow just forward
    // of the previous animation.
    const offsetX = 0.01;

    if (recap.driveDirection() === NFLPlayRecapVO.LEFT_TO_RIGHT) {
      return recap.startingYardLine() + recap.passDistance() + offsetX;
    }

    return recap.startingYardLine() - recap.passDistance() - offsetX;
  }

  /**
   * Returns the starting line of the rush.
   * @return {number}
   */
  getRushEndingYardLine(recap) {
    return recap.endingYardLine();
  }

  play(recap, field) {
    // TODO: Skip the rush arrow animation unless the rush distance
    // is long enough to display the minimum arrow. This is a little
    // wonky and should be thought through more.
    if (recap.isTurnover() || recap.rushDistance() <= 0.03) {
      return Promise.resolve();
    }

    const arrowStart = this.getRushStartingYardLine(recap);
    const arrowEnd = this.getRushEndingYardLine(recap);
    const svg = this.createArrow(field, arrowStart, arrowEnd);

    field.addChild(svg, 0, 0, 20);

    return new Promise((resolve) => {
      setTimeout(() => resolve(), 200);
    });
  }
}
