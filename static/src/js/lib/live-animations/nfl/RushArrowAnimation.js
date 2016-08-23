import LiveAnimation from './LiveAnimation';
import {createPath, createSVGElement} from './svgTools';
import NFLPlayRecapVO from './NFLPlayRecapVO';

export default class RushArrowAnimation extends LiveAnimation {
    
    /**
     * Returns an SVG arrow based on the provided field and
     * starting/ending yard lines.
     */
    createArrow (field, startingYardLine, endingYardLine, color = '#dedede', opacity = .75) {
        
        let barStart = startingYardLine;
        let barEnd = endingYardLine;
        let barTop = .38;
        let barBottom = .42;

        let tipWidth = .02;
        let tipHeight = .04;
        let tipTop = barTop - tipHeight;
        let tipPointY = .40;
        let tipPointX = barEnd;
        let tipBottom = barBottom + tipHeight;

        // Substract or add the width of the tip to the end
        // of the bar based on the arrows direction.
        if (barStart > barEnd) {
            barEnd += tipWidth;
        } else {
            barEnd -= tipWidth;
        }
        
        let points = [
            field.getFieldPos(barStart, barTop),
            field.getFieldPos(barEnd, barTop),
            // Begin tip of arrow
            field.getFieldPos(barEnd, tipTop),
            field.getFieldPos(tipPointX, tipPointY),
            field.getFieldPos(barEnd, tipBottom),
            // End tip of arrow
            field.getFieldPos(barEnd, barBottom),
            field.getFieldPos(barStart, barBottom)
        ].map(pt => [pt.x, pt.y]);

        let arrow = createPath(points);
        arrow.setAttribute('style', `fill:${color};fill-opacity:${opacity}`);

        let shadow = createPath(points);
        shadow.setAttribute('style', 'fill:#000;fill-opacity:.25;');
        shadow.setAttribute('transform', 'translate(-2,6)');

        let svg = createSVGElement(field.getWidth(), field.getHeight());
        svg.style.display = 'block';
        svg.appendChild(shadow);
        svg.appendChild(arrow);

        return svg;
    }

    /**
     * Returns the starting line of the rush.
     * @return {number}
     */
    getRushStartingYardLine (recap) {
        // Define a slight offset to help move the arrow just forward
        // of the previous animation.
        let offsetX = .01;

        if (recap.driveDirection() == NFLPlayRecapVO.LEFT_TO_RIGHT) {
            return recap.startingYardLine() + recap.passDistance() + offsetX;
        } else {
            return recap.startingYardLine() - recap.passDistance() - offsetX;
        }
    }

    /**
     * Returns the starting line of the rush.
     * @return {number}
     */
    getRushEndingYardLine (recap) {
        return recap.endingYardLine();
    }

    play (recap, field) {
        
        // TODO: Skip the rush arrow animation unless the rush distance
        // is long enough to display the minimum arrow. This is a little
        // wonky and should be thought through more.
        if (recap.isTurnover() || recap.rushDistance() <= .03) {
            return Promise.resolve();
        }

        let arrowStart = this.getRushStartingYardLine(recap);
        let arrowEnd = this.getRushEndingYardLine(recap);

        let svg = this.createArrow(field, arrowStart, arrowEnd);
        field.addChild(svg, 0, 0, 20);

        return new Promise((resolve, reject) => {
            setTimeout(() => resolve(), 200);
        });
    }
}
