import React from 'react';
import PureRenderMixin from 'react-addons-pure-render-mixin';
import { humanizeCurrency } from '../../lib/utils/currency';

/**
 * Responsible for rendering the scoreboard navigation user info section.
 */
const NavScoreboardUserInfo = React.createClass({

  propTypes: {
    name: React.PropTypes.string.isRequired,
    balance: React.PropTypes.oneOfType([
      React.PropTypes.string,
      React.PropTypes.number,
    ]),
  },

  mixins: [PureRenderMixin],

  render() {
    const { name, balance } = this.props;

    return (
      <div className="cmp-nav-scoreboard--user-info">
        <div className="name">{name}</div>
        <a href="/account/deposits/" className="add-funds" className="balance">
          <span className="balance-amount">{humanizeCurrency(balance, false)}</span>
          <span className="add-funds">ADD FUNDS</span>
        </a>
      </div>
    );
  },

});


export default NavScoreboardUserInfo;
