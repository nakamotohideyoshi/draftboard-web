export const clip = {
  frame_width: 180,
  frame_height: 100,
  length: 36,
  registration_x: 148,
  registration_y: 76,
  cuepoints: [
    {
      name: 'avatar',
      in: 35,
      data: { x: 122, y: 20, in: 35, name: 'receiver' },
    },
    {
      name: 'catch',
      in: 36,
      data: { x: 20, y: 20 },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-side-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-side-red.png'),
    both: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-side-white.png'),
  },
};
