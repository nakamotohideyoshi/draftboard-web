import Raven from 'raven-js';
import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import renderComponent from '../../lib/render-component';
import { fetchWithdrawForm, withdrawFormCompleted } from '../../actions/payments';
import { verifyLocation, fetchUser } from '../../actions/user';
const { Provider, connect } = ReactRedux;
import log from '../../lib/logging';


function mapStateToProps(state) {
  return {
    errors: state.payments.withdrawalFormErrors,
    isWithdrawing: state.payments.isWithdrawing,
    gidxWithdrawForm: state.payments.gidx.withdrawForm,
    merchantSessionId: state.payments.gidx.withdrawForm.merchantSessionId,
  };
}


function mapDispatchToProps(dispatch) {
  return {
    fetchUser: () => dispatch(fetchUser()),
    verifyLocation: () => dispatch(verifyLocation()),
    fetchWithdrawForm: (options) => dispatch(fetchWithdrawForm(options)),
    withdrawFormCompleted: (merchatSessionId) => dispatch(withdrawFormCompleted(merchatSessionId)),
  };
}


const Withdrawals = React.createClass({

  propTypes: {
    errors: React.PropTypes.object.isRequired,
    fetchWithdrawForm: React.PropTypes.func.isRequired,
    gidxWithdrawForm: React.PropTypes.object.isRequired,
    isWithdrawing: React.PropTypes.bool.isRequired,
    verifyLocation: React.PropTypes.func.isRequired,
    fetchUser: React.PropTypes.func.isRequired,
    merchantSessionId: React.PropTypes.string,
    withdrawFormCompleted: React.PropTypes.func.isRequired,
  },


  getDefaultProps() {
    return {
      isWithdrawing: false,
    };
  },


  componentDidMount() {
    // These functions are needed for the GIDX embed script.
    window.gidxServiceSettings = () => {
      window.gidxBuildSteps = true;
      // this is the dom object (div) where the cashier/registration service should be embedded
      // son the page.
      window.gidxContainer = '#GIDX_ServiceContainer';
    };

    window.gidxServiceStatus = (service, action, json) => {
      // If the withdraw process is finished, send a message to our server to withdraw funds from the
      // user's account.
      if (service === 'cashierFinalize-plate' && action === 'end') {
        const appState = store.getState();
        const msid = appState.payments.gidx.withdrawForm.merchantSessionId;

        if (!msid) {
          // If we don't have a session id, something went wrong so report it to sentry.
          Raven.captureMessage('MerchantSessionId missing!', {
            extra: {
              gidx: appState.payments.gidx,
              json,
            },
            level: 'error',
          });

          return;
        }

        // Dispatch the init withdraw event which will send a request to our server to create
        // a withdraw for the user.
        store.dispatch(withdrawFormCompleted(msid));
      }
    };

    window.gidxErrorReport = (error, errorMsg) => {
        // Error messages will be sent here by the GIDX Client Side Service
      log.error('======= gidxErrorReport =========');
      // send errors to Sentry.
      Raven.captureMessage(errorMsg, {
        error,
        level: 'error',
      });
      log.error(error, errorMsg);
    };

    // This never works. wtf.
    window.gidxNextStep = () => {
      log.info('gidxNextStep');
    };

    this.props.fetchUser();
    // First check if the user's location is valid. they will be redirected if
    // it isn't.
    this.props.verifyLocation();
  },


  componentDidUpdate(prevProps) {
    // If it's the first time we've recieved the form embed...
    if (!prevProps.gidxWithdrawForm.formEmbed && this.props.gidxWithdrawForm.formEmbed) {
      // This is some hack-ass shit.
      // In order to embed and run a script, you have to do it this way.
      const scriptTag = document.querySelector('#GIDX script');
      const newScriptTag = document.createElement('script');

      newScriptTag.type = 'text/javascript';
      newScriptTag.src = scriptTag.src;

      for (let i = 0; i < scriptTag.attributes.length; i++) {
        const a = scriptTag.attributes[i];
        newScriptTag.setAttribute(a.name, a.value);
      }
      this.refs.originalEmbed.remove();
      this.refs.GIDX_embed.append(newScriptTag);
    }
  },


  handleWithdraw(event) {
    if (!this.props.gidxWithdrawForm.isFetching) {
      event.preventDefault();
      // Fetch the gidx drop-in form.
      this.props.fetchWithdrawForm({ amount: this.refs.amount.value });
    }
  },

  // renderErrors(errors) {
  //   const errorList = [];
  //
  //   forEach(errors, (error, index) => {
  //     errorList.push(<p key={index} className="form-field-message__description">{ error }</p>);
  //   });
  //
  //   if (!errorList.length) {
  //     return '';
  //   }
  //
  //   return (
  //     <div className="form-field-message form-field-message--error form-field-message--settings">
  //       { errorList }
  //     </div>
  //   );
  // },

  renderAmountForm() {
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
                step="0.01"
              />
            </span>
          </div>

          <input ref="submit" type="submit" className="button button--gradient" value="Continue..." />
        </fieldset>
        </form>
      </div>
    );
  },

  render() {
    //  If we don't have a form embed, show the amount selector form.
    if (!this.props.gidxWithdrawForm.formEmbed) {
      return (
        this.renderAmountForm()
      );
    }

    // If we do, show the gidx drop-in.
    return (
      <div className="cmp-account-withdrawals">

        <div id="DepositAmountDisplay"></div>
        <div id="GIDX_ServiceContainer"></div>

        <div id="GIDX">
          <div ref="GIDX_embed">
            <div className="loading-placeholder" data-gidx-script-loading="true">
              Initializing secure withdraw process...
            </div>

            <div
              id="GIDX_embed_hidden"
              ref="originalEmbed"
              dangerouslySetInnerHTML={{ __html: this.props.gidxWithdrawForm.formEmbed }}
            ></div>
          </div>
        </div>

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
