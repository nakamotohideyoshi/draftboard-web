export const clip = {
  frame_width: 180,
  frame_height: 100,
  length: 36,
  registration_x: 148,
  registration_y: 76,
  cuepoints: [
    {
      name: 'avatar',
      in: 28,
      data: { x: 112, y: 20, in: 28, name: 'receiver' },
    },
    {
      name: 'catch',
      in: 29,
      data: { x: 126, y: 10 },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-side-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-side-red.png'),
    both: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-side-white.png'),
  },
};
