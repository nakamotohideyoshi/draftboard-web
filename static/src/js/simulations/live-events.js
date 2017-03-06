'use strict';


// Script that takes stored events in json and randomizes sending them via socket.io
// Let Craig know if you want to do this and he'll hook you up with the live-events.json, as it's 5MB
// don't want to put it in the repo

var io = require('socket.io')(5838);

io.on('connection', function (socket) {
  var history = require('../test/data/live-events');
  var i = 0;

  var nextSet = function() {
    // limit next set to random amount between 5 and 10 above i
    var end = i + Math.floor(Math.random() * 5) + 5;

    // check it's less than the length of items
    end = (end > history.length) ? history.length : end;

    console.log(end);

    for (var j = i; j < end; j++) {
      socket.emit('event', history[j]);
    }

    // set i for next set, then run in a couple seconds
    i = end;
    setTimeout(nextSet, 2500);
  };

  nextSet();
});
