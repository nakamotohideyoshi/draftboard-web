import ClipWithAvatar from '../clips/ClipWithAvatar';
import { clip as basketMadeZone1 } from '../clips/nba/basket-made-zone-1';
import { clip as basketMadeZone3 } from '../clips/nba/basket-made-zone-3';
import { clip as basketMissedZone1 } from '../clips/nba/basket-missed-zone-1';
import { clip as basketMissedZone3 } from '../clips/nba/basket-missed-zone-3';
import { clip as basketMissedZone5 } from '../clips/nba/basket-missed-zone-5';
import { clip as blockDunk } from '../clips/nba/block-dunk';
import { clip as blockJumpShotZone1 } from '../clips/nba/block-jump-shot-zone-1';
import { clip as blockJumpShotZone2 } from '../clips/nba/block-jump-shot-zone-2';
import { clip as blockJumpShotZone3 } from '../clips/nba/block-jump-shot-zone-3';
import { clip as blockJumpShotZone4 } from '../clips/nba/block-jump-shot-zone-4';
import { clip as blockJumpShotZone5 } from '../clips/nba/block-jump-shot-zone-5';
import { clip as blockLayup } from '../clips/nba/block-layup';
import { clip as dunkClip } from '../clips/nba/dunk';
import { clip as freeThrow } from '../clips/nba/free-throw';
import { clip as jumpShotZone1 } from '../clips/nba/jump-shot-zone-1';
import { clip as jumpShotZone2 } from '../clips/nba/jump-shot-zone-2';
import { clip as jumpShotZone3 } from '../clips/nba/jump-shot-zone-3';
import { clip as jumpShotZone4 } from '../clips/nba/jump-shot-zone-4';
import { clip as jumpShotZone5 } from '../clips/nba/jump-shot-zone-5';
import { clip as layupZone3 } from '../clips/nba/layup-zone-3';
import { clip as reboundZone3 } from '../clips/nba/rebound-zone-3';
import { clip as stealZone2 } from '../clips/nba/steal-zone-2';
import { clip as stealZone3 } from '../clips/nba/steal-zone-3';
import { clip as stealZone4 } from '../clips/nba/steal-zone-4';

const plays = {
  basket_made_zone_1: basketMadeZone1,
  basket_made_zone_2: basketMadeZone3,
  basket_made_zone_3: basketMadeZone3,
  basket_made_zone_4: basketMadeZone3,
  basket_made_zone_5: basketMadeZone1,
  basket_missed_zone_1: basketMissedZone1,
  basket_missed_zone_2: basketMissedZone1,
  basket_missed_zone_3: basketMissedZone3,
  basket_missed_zone_4: basketMissedZone5,
  basket_missed_zone_5: basketMissedZone5,
  dunk: dunkClip,
  freethrow: freeThrow,
  jumpshot_zone_1: jumpShotZone1,
  jumpshot_zone_2: jumpShotZone2,
  jumpshot_zone_3: jumpShotZone3,
  jumpshot_zone_4: jumpShotZone4,
  jumpshot_zone_5: jumpShotZone5,
  rebound: reboundZone3,
  layup: layupZone3,
  steal_zone_1: stealZone2,
  steal_zone_2: stealZone2,
  steal_zone_3: stealZone3,
  steal_zone_4: stealZone4,
  steal_zone_5: stealZone4,
  block_dunk: blockDunk,
  block_layup: blockLayup,
  block_jumpshot_zone_1: blockJumpShotZone1,
  block_jumpshot_zone_2: blockJumpShotZone2,
  block_jumpshot_zone_3: blockJumpShotZone3,
  block_jumpshot_zone_4: blockJumpShotZone4,
  block_jumpshot_zone_5: blockJumpShotZone5,
};

export function getClip(play) {
  const clip = plays[play];

  if (!clip) {
    throw new Error(`Unknown clip "${play}"`);
  } else {
    return new ClipWithAvatar(clip);
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
