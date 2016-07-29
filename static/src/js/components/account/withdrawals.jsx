import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import renderComponent from '../../lib/render-component';
import { withdraw } from '../../actions/payments';

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
    this.props.onWithdraw({
      amount: this.refs.amount.value,
      email: this.refs.email.value,
      ssn: this.refs.ssn.value,
    });
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
                ref="amount"
                className="form-field__text-input"
                type="text"
                name="amount"
                id="amount"
                placeholder="700"
                required
              />
            </span>
          </div>

          <div className="form-field form-field--with-help">
            <label className="form-field__label" htmlFor="paypal-email">Withdraw Method</label>
            <div className="form-field__content">
              <p className="form-field__info">
                You may receive your withdraw thru PayPal or a mailed check. Mailed checks may take
                between 7-12 business days to arrive.
              </p>

              <input
                ref="email"
                className="form-field__text-input"
                type="email"
                id="paypal-email"
                name="paypal-email"
                placeholder="Paypal associated email address..."
              />
            </div>
          </div>


          <div className="form-field form-field--with-help">
            <label className="form-field__label" htmlFor="ssn">SSN</label>
            <div className="form-field__content">
              <p className="form-field__info">
                Your Social Security Number must be provided for tax purposes.
              </p>

              <input
                ref="ssn"
                className="form-field__text-input"
                type="text"
                id="ssn"
                name="ssn"
              />
            </div>
          </div>

          <input type="submit" className="button button--flat-alt1" value="Withdraw" />
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
