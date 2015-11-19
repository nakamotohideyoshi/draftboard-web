'use strict';

import React from 'react';
const ReactRedux = require('react-redux')
const store = require('../../store')
const renderComponent = require('../../lib/render-component');

import {fetchUser} from '../../actions/user'


const Sidebar = React.createClass({

  propTypes: {
    user: React.PropTypes.object.isRequired,
    fetchUser: React.PropTypes.func.isRequired
  },

  componentWillMount() {
    this.props.fetchUser()
  },

  render() {
    return (
      <div>
        <header className="settings-sidebar-actions">
          <h1>My Account</h1>
          <a className="sign-out" href="#">Sign Out</a>
        </header>

        <section className="balance-summary">
          <h2>
            <sup>Current Balance</sup>
            <span className="currency">$</span>{this.props.user.balance}
          </h2>

        <hr/>
          <h2>
            <sup>Pending Bonus</sup>
            <span className="currency">$</span>{this.props.user.bonus}
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
  }

});


let {Provider, connect} = ReactRedux;


function mapStateToProps(state) {
  return {
    user: state.user.user
  };
}


function mapDispatchToProps(dispatch) {
  return {
    fetchUser: () => dispatch(fetchUser())
  }
}


var SidebarConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(Sidebar);


renderComponent(
  <Provider store={store}>
    <SidebarConnected />
  </Provider>,
  '#account-sidebar'
);


export default SidebarConnected;
