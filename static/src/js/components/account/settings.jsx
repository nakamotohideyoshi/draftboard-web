import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import renderComponent from '../../lib/render-component';
import { updateUserEmailPass, fetchEmailNotificationSettings, updateEmailNotificationSettings,
  fetchUser }
  from '../../actions/user';
import EmailPassForm from './subcomponents/email-pass-form.jsx';
import SettingsEmailNotifications from './subcomponents/settings-email-notifications.jsx';
import Identity from './subcomponents/identity.jsx';
const { Provider, connect } = ReactRedux;


function mapStateToProps(state) {
  return {
    username: state.user.username,
    identity: state.user.user.identity,
    user: state.user.user,
    infoFormErrors: state.user.infoFormErrors,
    emailPassFormErrors: state.user.emailPassFormErrors,
    notificationSettings: state.user.notificationSettings,
    emailNotificationFormErrors: state.user.notificationSettings.emailErrors,
  };
}

function mapDispatchToProps(dispatch) {
  return {
    updateUserEmailPass: (formData) => dispatch(updateUserEmailPass(formData)),
    updateEmailNotificationSettings: (formData) => dispatch(updateEmailNotificationSettings(formData)),
    fetchEmailNotificationSettings: () => dispatch(fetchEmailNotificationSettings()),
    fetchUser: () => dispatch(fetchUser()),
  };
}


/**
 * The user settings panel in the account section.
 */
const Settings = React.createClass({

  propTypes: {
    user: React.PropTypes.object.isRequired,
    username: React.PropTypes.string.isRequired,
    notificationSettings: React.PropTypes.object.isRequired,
    identity: React.PropTypes.object,
    infoFormErrors: React.PropTypes.object.isRequired,
    emailPassFormErrors: React.PropTypes.object.isRequired,
    updateUserEmailPass: React.PropTypes.func.isRequired,
    // updateUserNotifications: React.PropTypes.func.isRequired,
    fetchEmailNotificationSettings: React.PropTypes.func.isRequired,
    updateEmailNotificationSettings: React.PropTypes.func.isRequired,
    emailNotificationFormErrors: React.PropTypes.array,
    fetchUser: React.PropTypes.func.isRequired,
  },

  componentWillMount() {
    // Fetch the user's notification settings & user information.
    this.props.fetchEmailNotificationSettings();
    this.props.fetchUser();
  },

  render() {
    return (
      <div>
        <EmailPassForm
          user={this.props.user}
          username={this.props.username}
          errors={this.props.emailPassFormErrors}
          updateUserEmailPass={this.props.updateUserEmailPass}
        />

        <legend className="form__legend">Notifications</legend>

        <SettingsEmailNotifications
          user={this.props.user}
          errors={this.props.emailNotificationFormErrors}
          handleSubmit={this.props.updateEmailNotificationSettings}
          emailNotificationSettings = {this.props.notificationSettings.email}
        />

        <legend className="form__legend">
          Identity Information
        </legend>

        <Identity
          identity={this.props.identity}
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
