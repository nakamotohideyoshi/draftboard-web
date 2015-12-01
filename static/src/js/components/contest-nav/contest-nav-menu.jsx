'use strict'

const React = require('react')

import * as AppActions from '../../stores/app-state-store.js'


/**
 * Responsible for rendering the contest-nav top-left hamburger menu.
 */
const ContestNavMenu = React.createClass({

  getInitialState() {
    return {shown: false}
  },

  componentWillMount() {
    this.setState({shown: false})
    window.addEventListener('click', this.handleWindowClick)
  },

  handleWindowClick(e) {
    // if the nav isn't showing then return
    if (this.state.shown === false) {
      return true
    }

    const navMain = document.querySelectorAll(".nav-main")[0]
    const navTrigger = document.querySelectorAll(".cmp-contest-nav--menu")[0]

    const targetInNav = navMain.contains(e.target) === true || navMain === e.target
    const targetInNavTrigger = navTrigger.contains(e.target) === true || navTrigger === e.target

    // if we are clicking in the nav or its trigger, then don't close
    if (targetInNav || targetInNavTrigger) {
      return true
    }

    this.handleToggleHamburgerMenu()
    return false
  },

  handleToggleHamburgerMenu() {
    if (this.state.shown) {
      this.setState({shown: false})
      AppActions.closeNavMain()
    } else {
      this.setState({shown: true})
      AppActions.openNavMain()
    }
  },

  render() {
    return (
      <div className="cmp-contest-nav--menu">
        <div className={"mobile-forum-hamburger" + (this.state.shown ? ' closed' : '')}
             onClick={this.handleToggleHamburgerMenu}>
          <svg viewBox="0 0 42 42"
               height="16" width="16" className="icon icon-hamburger">
            <g>
              <path className="line-top" d="M3,13h36" fill="none"
                    stroke="white" strokeLinejoin="bevel" strokeWidth="3"></path>
              <path className="line-middle" d="M3,21h36" fill="none"
                    stroke="white" strokeLinejoin="bevel" strokeWidth="3"></path>
              <path className="line-bottom" d="M3,28h36" fill="none"
                    stroke="white" strokeLinejoin="bevel" strokeWidth="3"></path>
            </g>
          </svg>
        </div>
      </div>
    )
  }

})


module.exports = ContestNavMenu
