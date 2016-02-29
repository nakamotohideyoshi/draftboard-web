import React from 'react';
const ReactRedux = require('react-redux');
const store = require('../../store');
const renderComponent = require('../../lib/render-component');
import { updateUserInfo, updateUserAddress, updateUserEmailPass, }
  from '../../actions/user';
import EmailPasssForm from './subcomponents/email-pass-form.jsx';

const SettingsBase = require('./subcomponents/settings-base.jsx');
const SettingsAddress = require('./subcomponents/settings-address.jsx');
const { Provider, connect } = ReactRedux;


function mapStateToProps(state) {
  return {
    user: state.user.user,
    infoFormErrors: state.user.infoFormErrors,
    addressFormErrors: state.user.addressFormErrors,
  };
}


function mapDispatchToProps(dispatch) {
  return {
    updateUserInfo: (postData) => dispatch(updateUserInfo(postData)),
    updateUserAddress: (postData) => dispatch(updateUserAddress(postData)),
    updateUserEmailPass: (postData) => dispatch(updateUserEmailPass(postData)),
  };
}


const Settings = React.createClass({

  propTypes: {
    user: React.PropTypes.object.isRequired,
    infoFormErrors: React.PropTypes.object.isRequired,
    addressFormErrors: React.PropTypes.object.isRequired,
    updateUserInfo: React.PropTypes.func.isRequired,
    updateUserEmailPass: React.PropTypes.func.isRequired,
    updateUserAddress: React.PropTypes.func.isRequired,
  },

  render() {
    return (
      <div>
        <EmailPasssForm
          user={this.props.user}
          errors={this.props.infoFormErrors}
          updateUserEmailPass={this.props.updateUserEmailPass}
        />

        <SettingsBase
          user={this.props.user}
          errors={this.props.infoFormErrors}
          updateUserEmailPass={this.props.updateUserEmailPass}
        />

        <legend className="form__legend">User Profile</legend>

        <SettingsAddress
          user={this.props.user}
          errors={this.props.addressFormErrors}
          onHandleSubmit={this.props.updateUserAddress}
        />

      </div>
    );
  },

});


const SettingsConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(Settings);


renderComponent(
  <Provider store={store}>
    <SettingsConnected />
  </Provider>,
  '#account-settings'
);


export default SettingsConnected;
