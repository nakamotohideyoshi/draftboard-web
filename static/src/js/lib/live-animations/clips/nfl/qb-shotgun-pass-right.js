export const clip = {
  frame_width: 140,
  frame_height: 90,
  length: 88,
  registration_x: 134,
  registration_y: 52,
  cuepoints: [
    {
      name: 'avatar',
      in: 87,
      data: { x: 83, y: 13, in: 87, name: 'quarterback' },
    },
    {
      name: 'pass',
      in: 88,
      data: { x: 20, y: 20 },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-pass-right-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-pass-right-red.png'),
    both: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-pass-right-white.png'),
  },
};
