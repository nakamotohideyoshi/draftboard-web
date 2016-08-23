import LiveAnimation from './LiveAnimation';
import RushArrowAnimation from './RushArrowAnimation';
import NFLPlayRecapVO from './NFLPlayRecapVO';

/**
 * ...
 */
export default class PassArrowAnimation extends LiveAnimation {
    
    /**
     * Returns the yard line the reception occurred at.
     * @return {number}
     */
    getReceptionYardLine (recap) {
        if (recap.driveDirection() == NFLPlayRecapVO.LEFT_TO_RIGHT) {
            return recap.startingYardLine() + recap.passDistance();
        } else {
            return recap.startingYardLine() - recap.passDistance();
        }
    }

    play (recap, field) {

        let r = new RushArrowAnimation();
        let arrowStart = recap.startingYardLine();
        let arrowEnd = this.getReceptionYardLine(recap);

        let arrow = r.createArrow(field, arrowStart, arrowEnd, '#00ff00', 1);
        field.addChild(arrow, 0, 0, 30);
        //TODO: draw arrow based on SVG.
        //TODO: draw arrow from starting yard to ending yard
        return super.play(recap, field);
    }
}
