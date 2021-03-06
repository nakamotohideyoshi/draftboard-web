export const clip = {
  name: 'qb-default-handoff-left',
  frame_width: 190,
  frame_height: 100,
  length: 65,
  registration_x: 148,
  registration_y: 80,
  cuepoints: [
    {
      name: 'avatar',
      in: 44,
      data: { x: 54, y: 14, type: 'receiver', pause: true },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-handoff-left-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-handoff-left-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-default-handoff-left-red.png'),
  },
};
