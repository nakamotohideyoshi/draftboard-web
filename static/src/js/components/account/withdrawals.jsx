import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import renderComponent from '../../lib/render-component';
import { withdraw } from '../../actions/payments';
import SSNMaskedInput from '../form-field/ssn.jsx';

const { Provider, connect } = ReactRedux;

function mapStateToProps(state) {
  return {
    errors: state.payments.withdrawalFormErrors,
  };
}


function mapDispatchToProps(dispatch) {
  return {
    onWithdraw: (postData) => dispatch(withdraw(postData)),
  };
}


const Withdrawals = React.createClass({

  propTypes: {
    errors: React.PropTypes.object.isRequired,
    onWithdraw: React.PropTypes.func.isRequired,
  },

  handleWithdraw(event) {
    event.preventDefault();
    // gather data
    this.props.onWithdraw({});
  },

  render() {
    return (
      <div>
        <form className="form" method="post" onSubmit={this.handleWithdraw}>
        <fieldset className="form__fieldset">
          <div className="form-field">
            <label className="form-field__label" htmlFor="amount">
              Withdraw Amount
            </label>

            <span className="input-symbol-dollar">
              <input
                className="form-field__text-input"
                type="text"
                name="amount"
                id="amount"
                placeholder="700"
                required
              />
            </span>
          </div>

          <div className="form-field">
            <label className="form-field__label form-field__label--twoline" htmlFor="ssn">
              SSN for Taxes<br />(1099 Misc.)
            </label>
            <SSNMaskedInput />
          </div>

          <div className="form-field form-field--with-help">
            <label className="form-field__label" htmlFor="notifications">Withdraw Method</label>
            <div className="form-field__content">
              <p className="form-field__info">
                You may receive your withdraw thru PayPal or a mailed check. Mailed checks may take
                between 7-12 business days to arrive.
              </p>

              <input
                className="form-field__text-input"
                type="email"
                id="paypal-email"
                name="paypal-email"
                placeholder="Paypal associated email address..."
              />
            </div>
          </div>

          <input type="submit" className="button--medium" value="Withdraw" />
        </fieldset>
        </form>
      </div>
    );
  },

});


const WithdrawalsConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(Withdrawals);


renderComponent(
  <Provider store={store}>
    <WithdrawalsConnected />
  </Provider>,
  '#account-withdrawals'
);


export default WithdrawalsConnected;
