import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import renderComponent from '../../lib/render-component';
import { updateUserInfo, updateUserEmailPass, updateUserNotifications } from '../../actions/user';
import EmailPasssForm from './subcomponents/email-pass-form.jsx';
import SettingsEmailNotifications from './subcomponents/settings-email-notifications.jsx';
import SettingsAddress from './subcomponents/settings-address.jsx';
const { Provider, connect } = ReactRedux;


function mapStateToProps(state) {
  return {
    username: state.user.username,
    user: state.user.info,
    infoFormErrors: state.user.infoFormErrors,
    emailPassFormErrors: state.user.emailPassFormErrors,
  };
}

function mapDispatchToProps(dispatch) {
  return {
    updateUserEmailPass: (postData) => dispatch(updateUserEmailPass(postData)),
    updateUserNotifications: (postData) => dispatch(updateUserNotifications(postData)),
    updateUserInfo: (postData) => dispatch(updateUserInfo(postData)),
  };
}


/**
 * The user settings panel in the account section.
 */
const Settings = React.createClass({

  propTypes: {
    user: React.PropTypes.object.isRequired,
    username: React.PropTypes.string.isRequired,
    infoFormErrors: React.PropTypes.object.isRequired,
    emailPassFormErrors: React.PropTypes.object.isRequired,
    updateUserInfo: React.PropTypes.func.isRequired,
    updateUserEmailPass: React.PropTypes.func.isRequired,
    updateUserNotifications: React.PropTypes.func.isRequired,
  },

  render() {
    return (
      <div>
        <EmailPasssForm
          user={this.props.user}
          username={this.props.username}
          errors={this.props.emailPassFormErrors}
          updateUserEmailPass={this.props.updateUserEmailPass}
        />

        <legend className="form__legend">Notifications</legend>

        <SettingsEmailNotifications
          user={this.props.user}
          errors={this.props.emailPassFormErrors}
          handleSubmit={this.props.updateUserNotifications}
        />

        <legend className="form__legend">User Profile</legend>

        <SettingsAddress
          info={this.props.user}
          errors={this.props.infoFormErrors}
          onHandleSubmit={this.props.updateUserInfo}
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
