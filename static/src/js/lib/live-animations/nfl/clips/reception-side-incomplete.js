export const clip = {
  name: 'reception-side-incomplete',
  frame_width: 225,
  frame_height: 100,
  length: 46,
  registration_x: 148,
  registration_y: 76,
  cuepoints: [
    {
      name: 'avatar',
      in: 28,
      data: { x: 112, y: 20, type: 'receiver' },
    },
    {
      name: 'catch',
      in: 29,
      data: { x: 126, y: 10 },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-side-incomplete-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-side-incomplete-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-side-incomplete-white.png'),
  },
};
