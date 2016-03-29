require('../../test-dom')()
import React from 'react'
import Sparkline from '../../../components/draft/sparkline.jsx'
import { expect } from 'chai'
import sd from 'skin-deep'
import {sum as _sum} from 'lodash'

const TestUtils = require('react-addons-test-utils');
const props = {points: [0, 34, -5, 56, 12, 1.5, -1.7, 0, 33]}


describe('Sparkline Component', function() {
  let vdom, instance

  beforeEach(function() {
    let tree = sd.shallowRender(React.createElement(Sparkline, props))
    instance = tree.getMountedInstance()
    vdom = tree.getRenderOutput()
  })


  it('should render a span and an svg', function() {
    expect(vdom.type).to.equal('span')
    expect(vdom.props.children.type).to.equal('svg')
  })


  it('should not render an svg if no points are provided', function() {
    // render without points.
    let tree = sd.shallowRender(React.createElement(Sparkline))
    instance = tree.getMountedInstance()
    vdom = tree.getRenderOutput()
    expect(vdom.type).to.equal('span')
    expect(vdom.hasOwnProperty('children')).to.equal(false)
  })


  it('should draw an average line', function() {
    let avgLine = vdom.props.children.props.children.props.children.filter(function(child) {
      return child.ref === 'average'
    })
    expect(avgLine.length).to.equal(1)
  })

  it('should draw an spark line', function() {
    let avgLine = vdom.props.children.props.children.props.children.filter(function(child) {
      return child.ref === 'spark'
    })
    expect(avgLine.length).to.equal(1)
  })

})
