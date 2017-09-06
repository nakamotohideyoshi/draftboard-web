export const clip = {
  name: 'reception-interception',
  frame_width: 180,
  frame_height: 130,
  length: 46,
  registration_x: 28,
  registration_y: 106,
  cuepoints: [
    {
      name: 'avatar',
      in: 36,
      data: { x: 86, y: 30, type: 'receiver', pause: true },
    },
    {
      name: 'catch',
      in: 34,
      data: { x: 86, y: 30 },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-interception-white.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-interception-white.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-interception-white.png'),
  },
};
