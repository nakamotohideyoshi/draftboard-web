import NBAClip from './NBAClip';
import data from './nbaClips';

export function getClip(play) {
  const file = data.plays[play];
  const clip = data.clips.filter(dataClip => dataClip.file.indexOf(file) !== -1);

  if (!clip.length) {
    throw new Error(`Unknown clip "${play}"`);
  } else {
    return new NBAClip(clip[0]);
  }
}

export function getBasketClip(made, zone = null) {
  const madeOrMissed = made ? 'made' : 'missed';
  try {
    return getClip(`basket_${madeOrMissed}_zone_${zone}`);
  } catch (error) {
    throw new Error(`Unknown basket "${madeOrMissed}" clip for zone "${zone}"`);
  }
}

export function getJumpshotClip(zone = null) {
  try {
    return getClip(`jumpshot_zone_${zone}`);
  } catch (error) {
    throw new Error(`Unknown player clip "jumpshot", "${zone}"`);
  }
}

export function getBlockClip(zone = null) {
  try {
    return getClip(`block_jumpshot_zone_${zone}`);
  } catch (error) {
    throw new Error(`Unknown player clip "block", "${zone}"`);
  }
}

export function getStealClip(zone = null) {
  try {
    return getClip(`steal_zone_${zone}`);
  } catch (error) {
    throw new Error(`Unknown player clip "steal", "${zone}"`);
  }
}
