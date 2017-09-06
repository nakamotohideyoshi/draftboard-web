export const clip = {
  name: 'qb-shotgun-handoff-right',
  frame_width: 200,
  frame_height: 120,
  length: 79,
  registration_x: 134,
  registration_y: 72,
  cuepoints: [
    {
      name: 'avatar',
      in: 52,
      data: { x: 66, y: 24, type: 'receiver', pause: true },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-handoff-right-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-handoff-right-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-handoff-right-red.png'),
  },
};
