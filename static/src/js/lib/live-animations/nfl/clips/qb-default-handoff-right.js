export const clip = {
  name: 'qb-default-handoff-right',
  frame_width: 190,
  frame_height: 100,
  length: 65,
  registration_x: 144,
  registration_y: 66,
  cuepoints: [
    {
      name: 'avatar',
      in: 44,
      data: { x: 57, y: 20, type: 'receiver', pause: true },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-handoff-right-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-handoff-right-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-handoff-right-red.png'),
  },
};
