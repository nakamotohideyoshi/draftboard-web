export const clip = {
  frame_width: 160,
  frame_height: 100,
  length: 96,
  registration_x: 158,
  registration_y: 76,
  cuepoints: [
    {
      name: 'avatar',
      in: 95,
      data: { x: 96, y: 26, in: 95, name: 'quarterback' },
    },
    {
      name: 'pass',
      in: 96,
      data: { x: 20, y: 20 },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-pass-left-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-pass-left-red.png'),
    both: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-pass-left-white.png'),
  },
};
