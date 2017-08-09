export const clip = {
  frame_width: 180,
  frame_height: 130,
  length: 46,
  registration_x: 28,
  registration_y: 106,
  avatars: [
    {
      name: 'receiver',
      x: 100,
      y: 30,
      in: 30,
    },
  ],
  cuepoints: [
    {
      name: 'catch',
      in: 30,
      data: { x: 20, y: 20 },
    },
  ],
  files: {
    both: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/reception-interception-white.png'),
  },
};
