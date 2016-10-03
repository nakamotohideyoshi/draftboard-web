import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import renderComponent from '../../lib/render-component';
import { withdraw } from '../../actions/payments';
import { verifyLocation } from '../../actions/user';
import forEach from 'lodash/forEach';
import classNames from 'classnames';
import PubSub from 'pubsub-js';
const { Provider, connect } = ReactRedux;


function mapStateToProps(state) {
  return {
    errors: state.payments.withdrawalFormErrors,
    isWithdrawing: state.payments.isWithdrawing,
  };
}


function mapDispatchToProps(dispatch) {
  return {
    onWithdraw: (postData) => dispatch(withdraw(postData)),
    verifyLocation: () => dispatch(verifyLocation()),
  };
}


const Withdrawals = React.createClass({

  propTypes: {
    errors: React.PropTypes.object.isRequired,
    onWithdraw: React.PropTypes.func.isRequired,
    isWithdrawing: React.PropTypes.bool.isRequired,
    verifyLocation: React.PropTypes.func.isRequired,
  },


  getDefaultProps() {
    return {
      isWithdrawing: false,
    };
  },


  componentWillMount() {
    // First check if the user's location is valid. they will be redirected if
    // it isn't.
    this.props.verifyLocation();
    PubSub.subscribe('account.withdrawSuccess', () => this.resetForm());
  },


  resetForm() {
    this.refs.amount.value = '';
    this.refs.email.value = '';
  },


  handleWithdraw(event) {
    if (!this.props.isWithdrawing) {
      event.preventDefault();
      // gather data
      this.props.onWithdraw({
        amount: this.refs.amount.value,
        email: this.refs.email.value,
      });
    }
  },

  renderErrors(errors) {
    const errorList = [];

    forEach(errors, (error, index) => {
      errorList.push(<p key={index} className="form-field-message__description">{ error }</p>);
    });

    if (!errorList.length) {
      return '';
    }

    return (
      <div className="form-field-message form-field-message--error form-field-message--settings">
        { errorList }
      </div>
    );
  },

  render() {
    const withdrawClasses = classNames(
      'button button--flat-alt1',
      { 'button--disabled': this.props.isWithdrawing }
    );

    return (
      <div className="cmp-account-withdrawals">
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
                type="number"
                name="amount"
                id="amount"
                placeholder="700"
                required
                min="5"
                max="1000"
              />
            </span>
            {this.renderErrors(this.props.errors.amount)}
          </div>

          <div className="form-field form-field--with-help">
            <label className="form-field__label" htmlFor="paypal-email">PayPal Email</label>
            <div className="form-field__content">
              <p className="form-field__info">
                You will receive your withdraw via PayPal. Enter the email associated with your PayPal account.
              </p>

              <input
                ref="email"
                className="form-field__text-input"
                type="email"
                id="paypal-email"
                name="paypal-email"
                placeholder="Paypal associated email address..."
                required
              />
            </div>
            {this.renderErrors(this.props.errors.email)}
          </div>

          <input ref="submit" type="submit" className={ withdrawClasses } value="Withdraw" />
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


// Export the React component (for testing).
module.exports = Withdrawals;
// Export the store-injected ReactRedux component.
export default WithdrawalsConnected;
