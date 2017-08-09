export const clip = {
  frame_width: 190,
  frame_height: 110,
  length: 13,
  registration_x: 90,
  registration_y: 84,
  cuepoints: [
    {
      name: 'avatar',
      in: 13,
      data: { x: 96, y: 32, in: 13, name: 'receiver' },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/kick-reception-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/kick-reception-red.png'),
    both: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/kick-reception-white.png'),
  },
};
