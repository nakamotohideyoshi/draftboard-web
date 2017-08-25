export const clip = {
  name: 'reception-short-side-incomplete',
  frame_width: 135,
  frame_height: 100,
  length: 20,
  registration_x: 64,
  registration_y: 76,
  cuepoints: [
    {
      name: 'avatar',
      in: 7,
      data: { x: 66, y: 24, type: 'receiver' },
    },
    {
      name: 'catch',
      in: 9,
      data: { x: 76, y: 30 },
    },
  ],
  files: {
    /* eslint-disable max-len */
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-short-side-incomplete-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-short-side-incomplete-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-short-side-incomplete-white.png'),
    /* eslint-enable max-len */
  },
};
