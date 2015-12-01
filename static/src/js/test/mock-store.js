"use strict";

import createLogger from 'redux-logger'
import thunkMiddleware from 'redux-thunk'
import { applyMiddleware } from 'redux'
import { expect } from 'chai'


export var ActionTypes = {
  INIT: '@@redux/INIT'
}


/**
 * Creates a mock of Redux store with middleware.
 */
export function mockStore(reducer, initialState, checks = [], done) {
  if (!Array.isArray(checks)) {
    throw new Error('expectedActions should be an array of expected actions.')
  }
  if (typeof done !== 'undefined' && typeof done !== 'function') {
    throw new Error('done should either be undefined or function.')
  }


  function mockStoreWithoutMiddleware() {
    var currentReducer = reducer
    var currentState = initialState
    var listeners = []
    var isDispatching = false


    function getState() {
      return currentState
    }


    function subscribe(listener) {
      listeners.push(listener)
      var isSubscribed = true

      return function unsubscribe() {
        if (!isSubscribed) {
          return
        }

        isSubscribed = false
        var index = listeners.indexOf(listener)
        listeners.splice(index, 1)
      }
    }


    function dispatch(action) {
      try {
        isDispatching = true
        currentState = currentReducer(currentState, action)
      } finally {
        isDispatching = false
      }

      listeners.slice().forEach(listener => listener())


      // NOT FROM CREATESTORE.JS
      // This is added in order to check the value of actions after being dispatched
      // We shift off the latest check and if it's a function we run it
      const check = checks.shift()
      try {
        if (typeof check === 'function') {
          check(action, getState())
        }

        if (done && !checks.length) {
          done()
        }

      } catch (e) {
        done(e)
      }

      return action
    }


    function replaceReducer(nextReducer) {
      currentReducer = nextReducer
      dispatch({ type: ActionTypes.INIT })
    }

    dispatch({ type: ActionTypes.INIT })

    return {
      dispatch,
      subscribe,
      getState,
      replaceReducer
    }
  }


  const loggerMiddleware = createLogger({
    logger: console,
    level: 'error'
  })


  const mockStoreWithMiddleware = applyMiddleware(
    thunkMiddleware // lets us #dispatch() functions
    // loggerMiddleware // neat middleware that logs actions in the console
  )(mockStoreWithoutMiddleware)


  return mockStoreWithMiddleware()
}
