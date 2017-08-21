export const clip = {
  name: 'reception-short-side',
  frame_width: 100,
  frame_height: 100,
  length: 11,
  registration_x: 64,
  registration_y: 76,
  cuepoints: [
    {
      name: 'avatar',
      in: 10,
      data: { x: 66, y: 24, name: 'receiver' },
    },
    {
      name: 'catch',
      in: 11,
      data: { x: 76, y: 30 },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-short-side-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-short-side-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-short-side-white.png'),
  },
};
