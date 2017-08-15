export const clip = {
  name: 'qb-shotgun-pass-left',
  frame_width: 160,
  frame_height: 100,
  length: 96,
  registration_x: 158,
  registration_y: 76,
  cuepoints: [
    {
      name: 'avatar',
      in: 80,
      data: { x: 68, y: 20, in: 80, name: 'quarterback' },
    },
    {
      name: 'pass',
      in: 94,
      data: { x: 84, y: 15 },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-pass-left-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-pass-left-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-pass-left-white.png'),
  },
};
