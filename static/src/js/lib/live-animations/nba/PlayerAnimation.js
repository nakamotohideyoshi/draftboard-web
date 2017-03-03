import AvatarAnimation from './AvatarAnimation';
import NBAPlayRecapVO from './NBAPlayRecapVO';
import LiveAnimation from '../LiveAnimation';
import { getBlockClip, getClip, getJumpshotClip, getStealClip } from './getClip';

export default class PlayerAnimation extends LiveAnimation {

  /**
   * Returns the NBAClip associated with the recap's play type.
   */
  getPlayerClip(recap, court) {
    const zone = court.getZoneAtPosition(recap.courtPosition(), recap.teamBasket()) + 1;

    switch (recap.playType()) {
      case NBAPlayRecapVO.BLOCKED_DUNK:
        return getClip('block_dunk');
      case NBAPlayRecapVO.BLOCKED_LAYUP:
        return getClip('block_layup');
      case NBAPlayRecapVO.BLOCKED_HOOKSHOT:
        return getClip('block_layup');
      case NBAPlayRecapVO.BLOCKED_JUMPSHOT:
        return getBlockClip(zone);
      case NBAPlayRecapVO.DUNK:
        return getClip('dunk');
      case NBAPlayRecapVO.FREETHROW:
        return getClip('freethrow');
      case NBAPlayRecapVO.LAYUP:
        return getClip('layup');
      case NBAPlayRecapVO.HOOKSHOT:
        return getClip('layup');
      case NBAPlayRecapVO.JUMPSHOT:
        return getJumpshotClip(zone);
      case NBAPlayRecapVO.REBOUND:
        return getClip('rebound');
      case NBAPlayRecapVO.STEAL:
        return getStealClip(zone);
      default:
        throw new Error(`Unknown clip for play type "${recap.playType()}"`);
    }
  }

  /**
   * Returns the player's x,y court position in pixels based on
   * the recap's playType.
   */
  getPlayCourtPos(recap, court) {
    const teamBasket = recap.teamBasket();
    const playType = recap.playType();

    // Provide static positions for play types that are specific to
    // the animation and not based on the recap's court position.
    const staticPositions = {
      [NBAPlayRecapVO.BLOCKED_DUNK]: { x: 0.075, y: 0.4 },
      [NBAPlayRecapVO.BLOCKED_LAYUP]: { x: 0.075, y: 0.4 },
      [NBAPlayRecapVO.BLOCKED_HOOKSHOT]: { x: 0.075, y: 0.4 },
      [NBAPlayRecapVO.DUNK]: court.getRimPos(teamBasket),
      [NBAPlayRecapVO.FREETHROW]: court.getFreethrowPos(teamBasket),
      [NBAPlayRecapVO.HOOKSHOT]: court.getRimPos(teamBasket),
      [NBAPlayRecapVO.LAYUP]: court.getRimPos(teamBasket),
      [NBAPlayRecapVO.REBOUND]: { x: 0.075, y: 0.4 },
    };

    const pos = staticPositions.hasOwnProperty(playType)
      ? staticPositions[playType]
      : recap.courtPosition();

    // Flip the x coordinate of static positions that were defined only for the
    // left basket.
    if (teamBasket === NBAPlayRecapVO.BASKET_RIGHT) {
      if (playType === NBAPlayRecapVO.REBOUND ||
          playType === NBAPlayRecapVO.BLOCKED_DUNK ||
          playType === NBAPlayRecapVO.BLOCKED_LAYUP ||
          playType === NBAPlayRecapVO.BLOCKED_HOOKSHOT) {
        pos.x = 1 - pos.x;
      }
    }

    return court.getPosition(pos.x, pos.y);
  }

  /**
   * Returns a collection of AvatarAnimations based on the provided recap
   * and clip. Only player types defined in both the clip and recap result in the
   * creation of an AvatarAnimation.
   */
  createAvatarsForClip(clip, recap, court) {
    // Returns an AvatarAnimation based on the provided Player obj.
    const createAvatarFromPlayerObj = playerObj => {
      const data = clip.avatar(playerObj.type);
      const avatar = new AvatarAnimation(playerObj.name, playerObj.id);

      // HACK: to reference this data further down the chain when it comes time
      // to position the avatar on the court and trigger its animation.
      avatar.name = data.name;
      avatar.in = data.in;
      avatar.x = data.x;
      avatar.y = data.y;

      return avatar;
    };

    // Adds the provided avatar to the court based on the clip's position.
    const addAvatarToCourt = avatar => {
      let { x: courtX, y: courtY } = this.getPlayCourtPos(recap, court);

      // Move the avatar to the same position as the clip.
      courtX -= clip.offsetX;
      courtY -= clip.offsetY;

      // Align the avatar center/bottom so the point of the marker points to
      // the correct x/y position.
      courtX -= avatar.getWidth() * 0.5;
      courtY -= avatar.getHeight();

      // Offset the avatar to correctly position it based on the clip.
      courtX += avatar.x * 0.5;
      courtY += avatar.y * 0.5;

      // Force the avatar above it's defined origin.
      courtY -= 20;

      court.addChild(avatar.getElement(), courtX, courtY);

      return avatar;
    };

    // Hides the avatar until it's ready to be displayed.
    const hideAvatar = avatar => {
      const avatarEl = avatar.getElement();
      avatarEl.style.display = 'none';
      return avatar;
    };

    return recap.players()
    .filter(player => clip.avatar(player.type) !== null)
    .map(createAvatarFromPlayerObj)
    .map(addAvatarToCourt)
    .map(hideAvatar);
  }

  /**
   * Returns a promise that resolves once all provided avatars have loaded.
   */
  loadAvatars(avatars = []) {
    return avatars.length >= 1
      ? Promise.all(avatars.map(avatar => avatar.load()))
      : Promise.resolve();
  }

  /**
   * Returns a promise that resolves once all avatars and the clip have played
   * through completey.
   */
  playClipAndAvatars(clip, avatars) {
    const clipIn = clip.curFrame;
    const clipOut = clipIn + (clip.length - 1);

    // Play through the clip and the corresponding avatars chronologically
    const sequences = avatars.sort((a, b) => a.in - b.in)
    .map(avatar => () => {
      const avatarIn = clipIn + avatar.in;
      const avatarEl = avatar.getElement();

      // Play the clip to the avatar's "in" frame, then trigger the avatar's
      // animation sequence.
      return clip.play(avatarIn)
        .then(() => {
          avatarEl.style.display = 'block';
          return avatar.play();
        }).then(() => {
          avatarEl.style.display = 'none';
          return avatar;
        });
    });

    return sequences.reduce((promise, fn) =>
      promise.then(fn), Promise.resolve()
    ).then(() => clip.play(clipOut));
  }

  play(recap, court) {
    const clip = this.getPlayerClip(recap, court);
    const avatars = this.createAvatarsForClip(clip, recap, court);

    if (recap.teamBasket() === NBAPlayRecapVO.BASKET_RIGHT) {
      clip.flip();
    }

    // Offset the player's clip by it's offset to make sure it accurately lines
    // up with the play position. The offsetX and offsetY act as a
    // registration point.
    let { x: clipX, y: clipY } = this.getPlayCourtPos(recap, court);
    clipX -= clip.offsetX;
    clipY -= clip.offsetY;

    return Promise.all([
      clip.load(recap.whichSide()), this.loadAvatars(avatars),
    ]).then(() => {
      court.addChild(clip.getElement(), clipX, clipY);
      return this.playClipAndAvatars(clip, avatars);
    });
  }
}
