export const clip = {
  name: 'qb-shotgun-scramble',
  frame_width: 200,
  frame_height: 90,
  length: 90,
  registration_x: 184,
  registration_y: 66,
  cuepoints: [
    {
      name: 'avatar',
      in: 30,
      data: { x: 97, y: 10, type: 'receiver' },
    },
  ],
  files: {
    mine: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-scramble-blue.png'),
    opponent: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-scramble-red.png'),
    none: require('../../../../../img/blocks/live-animation-stage/nfl/sequences/qb-shotgun-scramble-red.png'),
  },
};
