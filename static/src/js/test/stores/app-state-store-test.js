"use strict";
require('../test-dom.js')();
let AppStateStore = require('../../stores/app-state-store');

var expect = require('chai').expect;


describe("AppStateStore", function() {

  afterEach(function() {
    document.body.innerHTML = '';
  });


  beforeEach(function() {
    document.body.innerHTML = '';

    // Reset the classes list for each test.
    AppStateStore.classes = [];
  });


  it("should start with an empty class list", function() {
    expect(AppStateStore.classes).to.be.empty;
  });


  it("should add a class to the classes list with addClass()", function() {
    AppStateStore.addClass('appstate-newclass');
    expect(AppStateStore.classes.length).to.equal(1);
    expect(AppStateStore.classes[0]).to.equal('appstate-newclass');

    // Add another and make sure it adds.
    // AppStateStore.addClass('appstate-anothernewclass');
    // expect(AppStateStore.classes.length).to.equal(2);
  });


  it("should remove a class from the classes list with removeClass()", function() {
    // Add a class.
    AppStateStore.addClass('appstate-newclass2');
    expect(AppStateStore.classes.length).to.equal(1);
    // Remove the class.
    AppStateStore.removeClass('appstate-newclass2');
    expect(AppStateStore.classes.length).to.equal(0);
  });


  it("should toggle classes", function() {
    // Add via toggle()
    AppStateStore.toggleClass('toggled');
    expect(AppStateStore.classes.length).to.equal(1);
    expect(AppStateStore.classes[0]).to.equal('toggled');

    // Remove via toggle()
    AppStateStore.toggleClass('toggled');
    expect(AppStateStore.classes.length).to.equal(0);
  });

});
