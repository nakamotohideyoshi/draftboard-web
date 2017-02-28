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
   * and clip. Only positions defined in both the clip and recap result in the
   * creation of an AvatarAnimation.
   */
  getAvatarsForClip(clip, recap, playPos, court) {
    const avatars = recap.players()
    .filter(player => clip.avatar(player.type) !== null)
    .map(player => {
      const avatarData = clip.avatar(player.type);

      const avatarView = new AvatarAnimation(player.name, player.id);
      avatarView.name = avatarData.name;
      avatarView.in = avatarData.in

      const avatarEl = avatarView.getElement();

      // Offset the avatar by its width and height so that the point of the marker
      // is bottom centered to the specified x and y position.
      let { x: courtX, y: courtY } = playPos;
      courtX -= avatarData.offset_x * 0.5 + avatarView.getWidth() * 0.5;
      courtY -= avatarData.offset_y * 0.5 + avatarView.getHeight();
      courtY -= 50; // Force the avatar above the player's head.

      // Temporarily hide the avatar, until it's told to play within 'playAvatars'
      avatarEl.style.display = 'none';
      court.addChild(avatarEl, courtX, courtY);

      return avatarView;
    });

    return avatars || [];
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
   * Returns a promise that resolves once all avatars have played.
   */
  playClipAndAvatars(clip, avatars) {
    const firstFrame = clip.curFrame;
    const lastFrame = firstFrame + (clip.length - 1);
    console.log('playClipAndAvatars:', firstFrame, lastFrame);
    const chain = avatars
    .sort((a, b) => a.in - b.in)
    .map(avatar => () => {
      const nextFrame = firstFrame + avatar.in;
      console.log(avatar.name, clip.curFrame, nextFrame);
      const el = avatar.getElement();
      el.style.display = 'none';

      return clip.play(nextFrame)
        .then(() => {
          console.log('avatar.play()', clip.curFrame, nextFrame);
          el.style.display = 'block';
          return avatar.play();
        }).then(() => {
          console.log('avatar.done', clip.curFrame, nextFrame);
          el.style.display = 'none';
        });
    });

    // Finish the sequence.
    chain.push(() => clip.play(lastFrame));

    return chain.reduce((promise, fn) =>
      promise.then(fn), Promise.resolve()
    );
  }

  play(recap, court) {
    const playPos = this.getPlayCourtPos(recap, court);
    const clip = this.getPlayerClip(recap, court);
    clip.curFrame = clip.getCuePoint(recap.whichSide());
    const avatars = this.getAvatarsForClip(clip, recap, playPos, court);

    if (recap.teamBasket() === NBAPlayRecapVO.BASKET_RIGHT) {
      clip.flip();
    }

    // Offset the player's clip by it's offset to make sure it accurately lines
    // up with the play position. The offsetX and offsetY act as a
    // registration point.
    let { x: clipX, y: clipY } = playPos;
    clipX -= clip.offsetX * 0.5;
    clipY -= clip.offsetY * 0.5;

    return Promise.all([
      clip.load(), this.loadAvatars(avatars),
    ])
    .then(() => court.addChild(clip.getElement(), clipX, clipY))
    .then(() => this.playClipAndAvatars(clip, avatars));
  }
}
