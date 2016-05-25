import Pusher from 'pusher-js';

var PusherDefinition = Pusher;

module.exports = {
  Pusher: PusherDefinition,
  EventDispatcher: PusherDefinition.EventsDispatcher,
  Util: PusherDefinition.Util,
  Members: PusherDefinition.Members
};
