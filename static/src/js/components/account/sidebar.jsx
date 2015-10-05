"use strict";

var React = require('react');
var Reflux = require('reflux');
var renderComponent = require('../../lib/render-component');

var AccountActions = require('../../actions/account-actions');
var AccountStore = require('../../stores/account-store');



var AccountSidebar = React.createClass({

  mixins: [
    Reflux.connect(AccountStore)
  ],

  componentWillMount: function() {
    // userBaseInfo takes argument force
    AccountActions.userBaseInfo(false);
  },

  render: function() {
    if (this.state.user !== undefined) {
      return (
        <div>
          <header className="settings-sidebar-actions">
            <h1>My Account</h1>
            <a className="sign-out" href="#">Sign Out</a>
          </header>

          <section className="balance-summary">
            <h2>
              <sup>Current Balance</sup>
              <span className="currency">$</span>{this.state.user.balance}
            </h2>

          <hr/>
            <h2>
              <sup>Pending Bonus</sup>
              <span className="currency">$</span>{this.state.user.bonus}
            </h2>

            <a
              href="/account/settings/deposit/"
              className="balance-summary--action button--large button--gradient-outline"
            >Deposit</a>
            <a
              href="/account/settings/withdrawals/"
              className="balance-summary--action button--gradient--background button--large button--gradient-outline"
            >Withdraw</a>
          </section>
        </div>
      );
    } else {
      return (
        <div> Loading...</div>
      );
    }
  }

});


renderComponent(<AccountSidebar />, '#account-sidebar');


module.exports = AccountSidebar;
