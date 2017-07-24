import React from 'react';
import Raven from 'raven-js';
import log from '../../../lib/logging.js';

// These functions are needed for the GIDX embed script.
window.gidxServiceSettings = () => {
  window.gidxBuildSteps = true;
  // this is the dom object (div) where the cashier/registration service should be embedded
  // son the page.
  window.gidxContainer = '#GIDX_ServiceContainer';
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


window.gidxServiceStatus = (service, action) => {
  // We want to skip the 1st WebReg step, so we have to auto-fill the
  // email confirmation field and push the submit button manually.
  if (service === 'idInitiate-plate' && action === 'start') {
    const emailField = document.querySelector('#EmailElement_EmailAddress');
    const emailFieldConfirm = document.querySelector('#EmailElement_EmailAddressConfirmMatch');
    emailFieldConfirm.value = emailField.value;
    const submitBtn = document.querySelector('#GIDX_ServiceContainer .gidx-controls .btn');
    submitBtn.click();
  }
};


const GidxIdentityForm = React.createClass({
  propTypes: {
    embed: React.PropTypes.string.isRequired,
    merchantSessionID: React.PropTypes.string.isRequired,
    checkUserIdentityVerificationStatus: React.PropTypes.func.isRequired,
    gidxFormInfo: React.PropTypes.object.isRequired,
  },

  componentDidMount() {
    const self = this;

    // This fires when the GIDX process is complete. We then call our server which makes
    // a request to GIDX to find out the status of the verification.
    window.gidxNextStep = () => {
      self.props.checkUserIdentityVerificationStatus(self.props.merchantSessionID);
    };

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
  },

  shouldComponentUpdate(nextProps) {
    // Only re-render if we get a new gidx status. We don't want something external to
    // re-render and destroy the embedded form.

    return this.props.gidxFormInfo.status !== nextProps.gidxFormInfo.status;
  },

  render() {
    if (this.props.gidxFormInfo.status === 'FAIL') {
      return (
        <div className="cmp-gidx-identity-form">
          <h3 className="cmp-modal__header">Unable Verify Your Identity</h3>
          <p className="description">Please contact support@draftboard.com with any questions.</p>
        </div>
      );
    }

    return (
      <div className="cmp-gidx-identity-form">
        <h3 className="cmp-modal__header">Account Verification</h3>
        <p className="description">
            Please confirm the info below.
        </p>

        <div id="DepositAmountDisplay"></div>
        <div id="GIDX_ServiceContainer"></div>

        <div id="GIDX">
          <div ref="GIDX_embed">
            <div data-gidx-script-loading="true">Loading...</div>

            <div
              id="GIDX_embed_hidden"
              ref="originalEmbed"
              dangerouslySetInnerHTML={{ __html: this.props.embed }}
            ></div>
          </div>
        </div>
      </div>
    );
  },
});

export default GidxIdentityForm;
