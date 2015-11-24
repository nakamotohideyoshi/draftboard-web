'use strict';

import React from 'react';
import PureRenderMixin from 'react-addons-pure-render-mixin';


/**
 * Responsible for rendering the scoreboard navigation user info section.
 */
const NavScoreboardUserInfo = React.createClass({

  mixins: [PureRenderMixin],

  propTypes: {
    name: React.PropTypes.string.isRequired,
    balance: React.PropTypes.string.isRequired
  },

  render() {
    const {name, balance} = this.props;

    return (
      <div className="cmp-nav-scoreboard--user-info">
        <div className="name">{name}</div>
        <div className="balance">
          {balance}
          <div className="add-funds">Add funds</div>
        </div>
      </div>
    );
  }

});


export default NavScoreboardUserInfo;
