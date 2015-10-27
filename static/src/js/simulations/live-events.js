'use strict';

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