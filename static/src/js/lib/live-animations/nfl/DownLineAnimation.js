import LiveAnimation from './LiveAnimation';
import {createPath, createSVGElement} from './svgTools';

export default class DownLineAnimation extends LiveAnimation {

    drawLine (field, yardLine, color = '#bdcc1a', opacity = .65) {
        // Determine the left and right position of the line based on
        // the width of the line. The width of the line is hardcoded
        // to approximately match the onfield graphics.
        let lineWidth = .003; 
        let lineLeft = yardLine - lineWidth;
        let lineRight = lineLeft + lineWidth;

        let points = [
            field.getFieldPos(lineLeft, 0),
            field.getFieldPos(lineRight, 0),
            field.getFieldPos(lineRight, 1),
            field.getFieldPos(lineLeft, 1),
        ].map(pt => [pt.x, pt.y]);
        
        let line = createPath(points);
        line.setAttribute('style', `fill:${color};fill-opacity:${opacity}`);

        let svg = createSVGElement(field.getWidth(), field.getHeight());
        svg.style.display = 'block';
        svg.appendChild(line);

        return svg;
    }

    play (recap, field) {
        let line = this.drawLine(field, recap.endingYardLine());
        field.addChild(line, 0, 0, 1);
        return super.play(recap, field);
    }
}
