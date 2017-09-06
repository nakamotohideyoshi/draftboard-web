export const clip = {
  name: 'kick-reception',
  frame_width: 190,
  frame_height: 110,
  length: 13,
  registration_x: 90,
  registration_y: 84,
  cuepoints: [
    {
      name: 'avatar',
      in: 12,
      data: { x: 96, y: 32, type: 'receiver', pause: true },
    },
    {
      name: 'catch',
      in: 10,
      data: { x: 96, y: 32 },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/kick-reception-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/kick-reception-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/kick-reception-white.png'),
  },
};
