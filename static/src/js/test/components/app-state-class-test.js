require('../test-dom')();
import * as AppActions from '../../stores/app-state-store.js'
var expect = require('chai').expect;


describe('AppStateClass Component', function() {

  beforeEach(function() {
    this.body = global.document.querySelector('body');
    // Reset any body classes.
    this.body.className = '';
    AppActions.classes = []
  });

  it("should add a className", function() {
    var classes = 'appstate-new-class';

    AppActions.addClass(classes);
    expect(this.body.className.trim()).to.equal('appstate-new-class');
  });


  it("should add multiple classNames", function() {
    var classes = 'appstate-new-class appstate-another-new-class appstate-another-nother-new-class';

    AppActions.addClass(classes);
    expect(this.body.className.trim()).to.equal(
      'appstate-new-class appstate-another-new-class appstate-another-nother-new-class'
    );
  });


  it("should append a className to existing classes", function() {
    var classes = 'appstate-new-class';
    this.body.className = 'existing-class';

    AppActions.addClass(classes);
    expect(this.body.className.trim()).to.equal('existing-class appstate-new-class');
  });


  it("should remove any existing appstate classes", function() {
    var classes = 'appstate-new-class';
    this.body.className = 'appstate-existing-class';

    AppActions.addClass(classes);
    expect(this.body.className.trim()).to.equal('appstate-new-class');
  });
});
