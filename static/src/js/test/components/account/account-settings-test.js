// 'use strict'

// require('../../test-dom')()
// const React =require('react')
// const ReactDOM = require('react-dom')
// const expect = require('chai').expect;

// const Settings = require('../../../components/account/settings.jsx')

// import reducers from '../../../reducers/index'
// import { mockStore } from '../../mock-store'


// describe('Settings component', function() {

//   beforeEach(function(done) {

//     const store = mockStore(reducers, {}, [], done)

//     var self = this

//     document.body.innerHTML = ''

//     this.targetElement = document.body.appendChild(document.createElement('div'))

//     this.settingsComponent = ReactDOM.render(
//       <Settings />,
//       this.targetElement,
//       function() {
//         self.settingsComponent = ReactDOM.findDOMNode(this);
//         done();
//       }
//     );
//   });

//   afterEach(function() {
//     document.body.innerHTML = ''
//   })

//   it('should render settings__base and settings__address inside the component', function() {
//     expect(
//       this.settingsComponent.querySelectorAll('.settings__base').length
//     ).to.equal(1)

//     expect(
//       this.settingsComponent.querySelectorAll('.settings__address').length
//     ).to.equal(1)
//   })

// });
