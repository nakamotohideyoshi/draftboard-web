export const clip = {
  frame_width: 180,
  frame_height: 90,
  length: 102,
  registration_x: 160,
  registration_y: 72,
  avatars: [
    {
      name: 'quarterback',
      x: 142,
      y: 26,
      in: 30,
    },
  ],
  cuepoints: [
    {
      name: 'pass',
      in: 102,
      data: { x: 20, y: 20 },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-middle-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-middle-red.png'),
    both: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-middle-white.png'),
  },
};
