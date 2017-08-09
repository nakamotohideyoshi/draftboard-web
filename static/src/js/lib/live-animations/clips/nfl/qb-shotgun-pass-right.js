export const clip = {
  frame_width: 140,
  frame_height: 90,
  length: 88,
  registration_x: 134,
  registration_y: 52,
  cuepoints: [
    {
      name: 'avatar',
      in: 78,
      data: { x: 58, y: 13, in: 78, name: 'quarterback' },
    },
    {
      name: 'pass',
      in: 88,
      data: { x: 56, y: 20 },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-pass-right-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-pass-right-red.png'),
    both: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-pass-right-white.png'),
  },
};
