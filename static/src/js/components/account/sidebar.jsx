import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store.js';
import renderComponent from '../../lib/render-component.js';
import { fetchUserInfo } from '../../actions/user';
const { Provider, connect } = ReactRedux;


function mapStateToProps(state) {
  return {
    user: state.user.info,
    cashBalance: window.dfs.user.cashBalance,
  };
}

function mapDispatchToProps(dispatch) {
  return {
    fetchUserInfo: () => dispatch(fetchUserInfo()),
  };
}


const Sidebar = React.createClass({

  propTypes: {
    user: React.PropTypes.object.isRequired,
    cashBalance: React.PropTypes.string,
    fetchUserInfo: React.PropTypes.func.isRequired,
  },

  componentWillMount() {
    this.props.fetchUserInfo();
  },

  render() {
    return (
      <div>
        <section className="balance-summary">
          <h2>
            <sup>Current Balance</sup>
            <span className="currency">$</span>{this.props.cashBalance}
          </h2>

        <hr />
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
  },

});


const SidebarConnected = connect(
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
