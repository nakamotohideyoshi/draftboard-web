import ClipWithAvatar from '../clips/ClipWithAvatar';
import { clip as kickReception } from './clips/kick-reception';
import { clip as qbDefaultHandoffLeft } from './clips/qb-default-handoff-left';
import { clip as qbDefaultHandoffRight } from './clips/qb-default-handoff-left';
import { clip as qbDefaultHandoffFumbleLeft } from './clips/qb-default-handoff-fumble-left';
import { clip as qbDefaultHandoffFumbleRight } from './clips/qb-default-handoff-fumble-right';
import { clip as qbDefaultPassDeepMiddle } from './clips/qb-default-pass-deep-middle';
import { clip as qbDefaultPassLeft } from './clips/qb-default-pass-left';
import { clip as qbDefaultPassMiddle } from './clips/qb-default-pass-middle';
import { clip as qbDefaultPassRight } from './clips/qb-default-pass-right';
import { clip as qbDefaultSack } from './clips/qb-default-sack';
import { clip as qbDefaultScramble } from './clips/qb-default-scramble';
import { clip as qbShotgunHandoffLeft } from './clips/qb-shotgun-handoff-left';
import { clip as qbShotgunHandoffRight } from './clips/qb-shotgun-handoff-right';
import { clip as qbShotgunHandoffShortLeft } from './clips/qb-shotgun-handoff-short-left';
import { clip as qbShotgunHandoffShortRight } from './clips/qb-shotgun-handoff-short-right';
import { clip as qbShotgunHandoffFumbleLeft } from './clips/qb-shotgun-handoff-fumble-left';
import { clip as qbShotgunHandoffFumbleRight } from './clips/qb-shotgun-handoff-fumble-right';
import { clip as qbShotgunPassLeft } from './clips/qb-shotgun-pass-left';
import { clip as qbShotgunPassMiddle } from './clips/qb-shotgun-pass-middle';
import { clip as qbShotgunPassRight } from './clips/qb-shotgun-pass-right';
import { clip as qbShotgunSack } from './clips/qb-shotgun-sack';
import { clip as qbShotgunScramble } from './clips/qb-shotgun-scramble';
import { clip as receptionInterception } from './clips/reception-interception';
import { clip as receptionBasket } from './clips/reception-basket';
import { clip as receptionBasketIncomplete } from './clips/reception-basket-incomplete';
import { clip as receptionShortBasket } from './clips/reception-short-basket';
import { clip as receptionShortBasketIncomplete } from './clips/reception-short-basket-incomplete';
import { clip as receptionShortSide } from './clips/reception-short-side';
import { clip as receptionShortSideIncomplete } from './clips/reception-short-side-incomplete';
import { clip as receptionSide } from './clips/reception-side';
import { clip as receptionSideIncomplete } from './clips/reception-side-incomplete';

const plays = {
  kick_reception: kickReception,
  reception_pass_left: receptionSide,
  reception_pass_left_incomplete: receptionSideIncomplete,
  reception_pass_middle: receptionBasket,
  reception_pass_middle_incomplete: receptionBasketIncomplete,
  reception_pass_right: receptionSide,
  reception_pass_right_incomplete: receptionSideIncomplete,
  reception_pass_short_left: receptionShortSide,
  reception_pass_short_left_incomplete: receptionShortSideIncomplete,
  reception_pass_short_middle: receptionShortBasket,
  reception_pass_short_middle_incomplete: receptionShortBasketIncomplete,
  reception_pass_short_right: receptionShortSide,
  reception_pass_short_right_incomplete: receptionShortSideIncomplete,
  reception_pass_deep_left: receptionBasket,
  reception_pass_deep_left_incomplete: receptionBasketIncomplete,
  reception_pass_deep_middle: receptionBasket,
  reception_pass_deep_middle_incomplete: receptionBasketIncomplete,
  reception_pass_deep_right: receptionBasket,
  reception_pass_deep_right_incomplete: receptionBasketIncomplete,
  reception_interception: receptionInterception,
  qb_shotgun_sack: qbShotgunSack,
  qb_shotgun_scramble_left: qbShotgunScramble,
  qb_shotgun_scramble_right: qbShotgunScramble,
  qb_shotgun_scramble_middle: qbShotgunScramble,
  qb_shotgun_handoff_left: qbShotgunHandoffLeft,
  qb_shotgun_handoff_middle: qbShotgunHandoffRight,
  qb_shotgun_handoff_right: qbShotgunHandoffRight,
  qb_shotgun_handoff_short_left: qbShotgunHandoffShortLeft,
  qb_shotgun_handoff_short_middle: qbShotgunHandoffShortRight,
  qb_shotgun_handoff_short_right: qbShotgunHandoffShortRight,
  qb_shotgun_handoff_fumble_left: qbShotgunHandoffFumbleLeft,
  qb_shotgun_handoff_fumble_middle: qbShotgunHandoffFumbleRight,
  qb_shotgun_handoff_fumble_right: qbShotgunHandoffFumbleRight,
  qb_shotgun_pass_left: qbShotgunPassLeft,
  qb_shotgun_pass_middle: qbShotgunPassMiddle,
  qb_shotgun_pass_right: qbShotgunPassRight,
  qb_shotgun_pass_deep_left: qbShotgunPassMiddle,
  qb_shotgun_pass_deep_middle: qbShotgunPassMiddle,
  qb_shotgun_pass_deep_right: qbShotgunPassMiddle,
  qb_shotgun_pass_short_left: qbShotgunPassLeft,
  qb_shotgun_pass_short_middle: qbShotgunPassMiddle,
  qb_shotgun_pass_short_right: qbShotgunPassRight,
  qb_default_sack: qbDefaultSack,
  qb_default_scramble_left: qbDefaultScramble,
  qb_default_scramble_right: qbDefaultScramble,
  qb_default_scramble_middle: qbDefaultScramble,
  qb_default_handoff_left: qbDefaultHandoffLeft,
  qb_default_handoff_middle: qbDefaultHandoffLeft,
  qb_default_handoff_right: qbDefaultHandoffRight,
  qb_default_handoff_short_left: qbDefaultHandoffLeft,
  qb_default_handoff_short_middle: qbDefaultHandoffLeft,
  qb_default_handoff_short_right: qbDefaultHandoffRight,
  qb_default_handoff_fumble_left: qbDefaultHandoffFumbleLeft,
  qb_default_handoff_fumble_middle: qbDefaultHandoffFumbleLeft,
  qb_default_handoff_fumble_right: qbDefaultHandoffFumbleRight,
  qb_default_pass_left: qbDefaultPassLeft,
  qb_default_pass_middle: qbDefaultPassMiddle,
  qb_default_pass_right: qbDefaultPassRight,
  qb_default_pass_deep_left: qbDefaultPassDeepMiddle,
  qb_default_pass_deep_middle: qbDefaultPassDeepMiddle,
  qb_default_pass_deep_right: qbDefaultPassDeepMiddle,
  qb_default_pass_short_left: qbDefaultPassLeft,
  qb_default_pass_short_middle: qbDefaultPassMiddle,
  qb_default_pass_short_right: qbDefaultPassRight,
};

/**
 * Returns a clip based on the provided play.
 */
export default function getClip(play) {
  const clip = plays[play];

  if (!clip) {
    throw new Error(`Unknown clip "${play}"`);
  } else {
    return new ClipWithAvatar(clip);
  }
}

/**
 * Returns a QB representing the provided formation, action, and side.
 * @param {string} formation    The play formation.
 * @param {string} action       The play action (handoff, scramble, etc.).
 * @param {string} side         The side of the field (left, middle, right).
 */
export function getQBClip(formation, action, side) {
  try {
    return getClip(`qb_${formation}_${action}_${side}`);
  } catch (error) {
    throw new Error(`Unknown QB animation "${formation}", "${action}", "${side}". ${error}`);
  }
}

/**
 * Returns a clip representing the QB being sacked from the specified formation.
 */
export function getQBSackClip(formation) {
  try {
    return getClip(`qb_${formation}_sack`);
  } catch (error) {
    throw new Error(`Unknown QB Sacked animation "${formation}"`);
  }
}

/**
 * Returns a reception representing the provided pass type and side.
 * @param {string} passType     The type of pass being caught.
 * @param {string} side         The side of the field (left, middle, right).
 */
export function getReceptionClip(passType, side) {
  try {
    return getClip(`reception_${passType}_${side}`);
  } catch (error) {
    throw new Error(`Unknown reception animation "${passType}", "${side}".`);
  }
}

/**
 * Returns an interception clip.
 */
export function getInterceptionClip() {
  try {
    return getClip('reception_interception');
  } catch (error) {
    throw new Error('Unknown interception animation.');
  }
}

export function getIncompleteReceptionClip(passType, side) {
  try {
    return getClip(`reception_${passType}_${side}_incomplete`);
  } catch (error) {
    return getReceptionClip(passType, side, false);
  }
}

/**
 * Returns a clip representing kick returns.
 */
export function getKickReturnClip() {
  try {
    return getClip('kick_reception');
  } catch (error) {
    throw new Error('A kick return clip has not been defined.');
  }
}
