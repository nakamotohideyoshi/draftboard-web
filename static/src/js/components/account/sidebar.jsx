import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store.js';
import renderComponent from '../../lib/render-component.js';
const { Provider, connect } = ReactRedux;
import { humanizeCurrency } from '../../lib/utils/currency.js';


function mapStateToProps(state) {
  return {
    cashBalance: state.user.cashBalance.amount,
  };
}


function mapDispatchToProps() {
  return {};
}


const Sidebar = (props) => (
  <div>
    <section className="balance-summary">
      <h2>
        <sup>Current Balance</sup>
        <span className="currency"></span>{ humanizeCurrency(props.cashBalance, false) }
      </h2>

      <a
        href="/account/deposits/"
        className="balance-summary--action button button--outline-alt1 button--med button--lrg-len"
      >Deposit</a>
      <a
        href="/account/withdraw/"
        className="balance-summary--action button button--gradient button--med button--lrg-len"
      >Withdraw</a>
    </section>
  </div>
);


Sidebar.propTypes = {
  cashBalance: React.PropTypes.number,
};


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
