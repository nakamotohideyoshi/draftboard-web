import LiveAnimation from './LiveAnimation';

/**
 * ...
 */
export default class OutroAnimation extends LiveAnimation {
    
    play (recap, field) {
        //TODO: Fade off all clips...
        return new Promise((resolve, reject) => {
            //DEBUG: Wait a second and then KO all the clips without a fade.
            setTimeout(() => {
                field.removeAll();
                resolve();
            }, 1500);
        });
    }
}
