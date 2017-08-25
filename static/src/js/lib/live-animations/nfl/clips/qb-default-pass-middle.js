export const clip = {
  name: 'qb-default-pass-middle',
  frame_width: 180,
  frame_height: 90,
  length: 102,
  registration_x: 160,
  registration_y: 72,
  cuepoints: [
    {
      name: 'avatar',
      in: 67,
      data: { x: 42, y: 20, type: 'quarterback' },
    },
    {
      name: 'pass',
      in: 90,
      data: { x: 66, y: 10 },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-middle-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-middle-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-middle-white.png'),
  },
};
