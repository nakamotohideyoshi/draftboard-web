export const clip = {
  frame_width: 180,
  frame_height: 130,
  length: 46,
  registration_x: 28,
  registration_y: 106,
  cuepoints: [
    {
      name: 'avatar',
      in: 36,
      data: { x: 86, y: 30, in: 36, name: 'receiver' },
    },
    {
      name: 'catch',
      in: 34,
      data: { x: 76, y: 20 },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-interception-white.png'),
    both: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-interception-white.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-interception-white.png'),
  },
};
