'use strict';

const React = require('react');

const AppActions = require('../../actions/app-actions');


/**
 * Responsible for rendering the contest-nav top-left hamburger menu.
 */
const ContestNavMenu = React.createClass({

  getInitialState() {
    return {shown: false};
  },

  handleToggleHamburgerMenu() {
    if (this.state.shown) {
      this.setState({shown: false});
      AppActions.closeNavMain();
    } else {
      this.setState({shown: true});
      AppActions.openNavMain();
    }
  },

  render() {
    return (
      <div className="cmp-contest-nav--menu">
        <div className={"mobile-forum-hamburger" + (this.state.shown ? ' closed' : '')}
             onClick={this.handleToggleHamburgerMenu}>
          <svg viewBox="0 0 42 42"
               height="30" width="30" className="icon icon-hamburger">
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
    );
  }

});


module.exports = ContestNavMenu;
