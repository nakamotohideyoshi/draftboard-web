export const clip = {
  name: 'qb-default-pass-right',
  frame_width: 150,
  frame_height: 90,
  length: 94,
  registration_x: 120,
  registration_y: 60,
  cuepoints: [
    {
      name: 'avatar',
      in: 81,
      data: { x: 48, y: 20, in: 81, name: 'quarterback' },
    },
    {
      name: 'pass',
      in: 84,
      data: { x: 40, y: 30 },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-right-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-right-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-pass-right-white.png'),
  },
};
