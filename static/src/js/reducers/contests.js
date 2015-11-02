"use strict";

const ActionTypes = require('../action-types');

const defaultContests = [
  {
    'id': 0,
    'title': '$150k NBA Championship',
    'winning': "$82",
    'position': '22',
    'entries': '1.8k'
  },
  {
    'id': 1,
    'title': '$150k NBA Championship',
    'winning': "$82",
    'position': '22',
    'entries': '1.8k'
  },
  {
    'id': 2,
    'title': '$150k NBA Championship',
    'winning': "$82",
    'position': '22',
    'entries': '1.8k'
  },
  {
    'id': 3,
    'title': '$150k NBA Championship',
    'winning': "$82",
    'position': '22',
    'entries': '1.8k'
  },
  {
    'id': 4,
    'title': '$150k NBA Championship',
    'winning': "$82",
    'position': '22',
    'entries': '1.8k'
  },
  {
    'id': 5,
    'title': '$150k NBA Championship',
    'winning': "$82",
    'position': '22',
    'entries': '1.8k'
  },
  {
    'id': 6,
    'title': '$150k NBA Championship',
    'winning': "$82",
    'position': '22',
    'entries': '1.8k'
  },
  {
    'id': 7,
    'title': '$150k NBA Championship',
    'winning': "$82",
    'position': '22',
    'entries': '1.8k'
  },
  {
    'id': 22,
    'title': '$150k NBA Championship',
    'winning': "$82",
    'position': '22',
    'entries': '1.8k'
  },
  {
    'id': 33,
    'title': '$150k NBA Championship',
    'winning': "$82",
    'position': '22',
    'entries': '1.8k'
  },
  {
    'id': 44,
    'title': '$150k NBA Championship',
    'winning': "$82",
    'position': '22',
    'entries': '1.8k'
  },
  {
    'id': 55,
    'title': '$150k NBA Championship',
    'winning': "$82",
    'position': '22',
    'entries': '1.8k'
  },
  {
    'id': 66,
    'title': '$150k NBA Championship',
    'winning': "$82",
    'position': '22',
    'entries': '1.8k'
  },
  {
    'id': 77,
    'title': '$150k NBA Championship',
    'winning': "$82",
    'position': '22',
    'entries': '1.8k'
  }
];

module.exports = function(state = defaultContests, action) {
  switch (action.type) {
  case ActionTypes.ADD_CONTEST:
    console.assert(action.contest, "No `contest` key in ADD_CONTEST action.");

    return [...state, action.contest];

  case ActionTypes.REMOVE_CONTEST:
    console.assert(action.id, "No `id` key in REMOVE_CONTEST action.");

    return state.filter((c) => {
      return c.id !== action.id;
    });

  case ActionTypes.UPDATE_CONTEST:
    console.assert(action.contest, "No `contest` key in UPDATE_CONTEST action.");

    return state.map((c) => {
      return c.id === action.contest.id ? action.contest : c;
    });

  default:
    return state;
  }
};

// -------------------------------------------------------------------
// Actions

// TODO: Define in `contest-actions.js`.
//
// function addContest(contest) {
//   return {type: ActionTypes.ADD_CONTEST, contest};
// }
//
// function updateContest(contest) {
//   return {type: ActionTypes.UPDATE_CONTEST, contest};
// }
//
// function removeContest(id) {
//   return {type: ActionTypes.REMOVE_CONTEST, id};
// }

// -------------------------------------------------------------------
// Updates

// TODO: Migrating store outside of components.
//
// const store = require('../store');
// store.dispatch(removeContest(10));
//
