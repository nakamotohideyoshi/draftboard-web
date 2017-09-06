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
      in: 62,
      data: { x: 38, y: 20, type: 'quarterback', pause: true },
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
