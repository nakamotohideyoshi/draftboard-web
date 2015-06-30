"use strict";

var expect = require('chai').expect;


describe("AppStateStore", function() {

  beforeEach(function() {
    this.AppStateStore = require('../../stores/app-state-store');
    // Reset the classes list for each test.
    this.AppStateStore.classes = [];
  });


  it("should start with an empty class list", function() {
    expect(this.AppStateStore.classes).to.be.empty;
  });


  it("should add a class to the classes list with addClass()", function() {
    this.AppStateStore.addClass('appstate-newclass');
    expect(this.AppStateStore.classes.length).to.equal(1);
    expect(this.AppStateStore.classes[0]).to.equal('appstate-newclass');

    // Add another and make sure it adds.
    this.AppStateStore.addClass('appstate-anothernewclass');
    expect(this.AppStateStore.classes.length).to.equal(2);
  });


  it("should remove a class from the classes list with removeClass()", function() {
    // Add a class.
    this.AppStateStore.addClass('appstate-newclass2');
    expect(this.AppStateStore.classes.length).to.equal(1);
    // Remove the class.
    this.AppStateStore.removeClass('appstate-newclass2');
    expect(this.AppStateStore.classes.length).to.equal(0);
  });


  it("should toggle classes", function() {
    // Add via toggle()
    this.AppStateStore.toggleClass('toggled');
    expect(this.AppStateStore.classes.length).to.equal(1);
    expect(this.AppStateStore.classes[0]).to.equal('toggled');

    // Remove via toggle()
    this.AppStateStore.toggleClass('toggled');
    expect(this.AppStateStore.classes.length).to.equal(0);
  });

});
