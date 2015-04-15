"use strict";

//jest.dontMock("../../../stores/contest-store.js");
jest.dontMock("../../../components/contest-list/contest-list.jsx");
jest.dontMock("../../../fixtures/contests.js");

var React, TestUtils, ContestListComponent, contestList, contestData;


describe("ContestList", function() {

  beforeEach(function() {
    React = require("react/addons");
    TestUtils = React.addons.TestUtils;
    ContestListComponent = require("../../../components/contest-list/contest-list.jsx");
    contestList = TestUtils.renderIntoDocument(<ContestListComponent />);
    contestData = require("../../../fixtures/contests.js");

  });

  it("should log hello world!", function() {
    console.log(contestList.state);
    contestList.state.contests = contestData;
    console.log(contestList.state);
    console.log("hello world!");
  });

});

