import LiveAnimation from './LiveAnimation';
import PassingPlayAnimation from './PassingPlayAnimation';
import RushingPlayAnimation from './RushingPlayAnimation';

/**
 * ...
 */
export default class NFLLivePlayAnimation extends LiveAnimation {

    /**
     * Returns a Live Animation based on the provided recap.
     * @param {NFLPlayRecapVO}  The recap.
     */
    getAnimation (recap) {
        if (recap.isPassingPlay()) {
            return new PassingPlayAnimation();
        } else if (recap.isRushingPlay()) {
            return new RushingPlayAnimation();
        } else {
            return null;
        }
    }

    /**
     * Plays the provided recap.
     * @param {NFLPlayRecapVO}  The recap.
     * @param {NFLField}        Field of play.
     */
    play (recap, field) {
        let animation = this.getAnimation(recap);

        if (!animation) {
            return Promise.reject('Unknown animation.');
        } else {
            return animation.play(recap, field);
        }
    }
}
