const data = require('../../../../img/blocks/live/nfl/sequences/clips.json');

/**
 * Returns a clip based on the provided fileName.
 * @param {string} formation    The play formation.
 * @param {string} action       The play action (handoff, scramble, etc.).
 * @param {string} side         The side of the field (left, middle, right).
 * @return {string|null}        The MP4 URI of the requested animation or null.
 */
export default function getClip (play) {
    let file = data.plays[play];
    let clip = data.clips.filter((clip) => {
        return clip.file == file;
    });

    if (!clip.length) {
        throw new Error(`Unknown clip "${play}"`);
    } else {
        return clip[0]
    }
}

/**
 * Returns a QB MP4 representing the provided formation, action, and side.
 * @param {string} formation    The play formation.
 * @param {string} action       The play action (handoff, scramble, etc.).
 * @param {string} side         The side of the field (left, middle, right).
 * @return {string|null}        The MP4 URI of the requested animation or null.
 */
export function getQBClip (formation, action, side) {
    try {
        return getClip(`qb_${formation}_${action}_${side}`);
    } catch (error) {
        throw new Error(`Unknown QB animation "${formation}", "${action}", "${side}".`);
    }
}

/**
 * Returns a reception MP4 representing the provided pass type and side.
 * @param {string} passType     The type of pass being caught.
 * @param {string} side         The side of the field (left, middle, right).
 * @return {string|null}        The MP4 URI of the requested animation or null.
 */
export function getReceptionClip (passType, side, isIntercepted = false) {
    try {
        return getClip(isIntercepted ? 'reception_interception' : `reception_${passType}_${side}`);
    } catch (error) {
        throw new Error(`Unknown reception animation "${passType}", "${side}", "${isIntercepted}".`);
    }
}
