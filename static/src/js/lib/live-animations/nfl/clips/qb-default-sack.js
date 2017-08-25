export const clip = {
  name: 'qb-default-sack',
  frame_width: 180,
  frame_height: 90,
  length: 75,
  registration_x: 160,
  registration_y: 72,
  cuepoints: [
    {
      name: 'avatar',
      in: 24,
      data: { x: 142, y: 26, type: 'quarterback' },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-sack-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-sack-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-sack-white.png'),
  },
};
