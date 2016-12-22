import React from 'react';
import * as ReactRedux from 'react-redux';
import store from '../../store';
import renderComponent from '../../lib/render-component';
import { updateUserInfo, updateUserEmailPass, fetchEmailNotificationSettings,
          updateEmailNotificationSettings }
  from '../../actions/user';
import EmailPassForm from './subcomponents/email-pass-form.jsx';
import SettingsEmailNotifications from './subcomponents/settings-email-notifications.jsx';
const { Provider, connect } = ReactRedux;


function mapStateToProps(state) {
  return {
    username: state.user.username,
    user: state.user.info,
    infoFormErrors: state.user.infoFormErrors,
    emailPassFormErrors: state.user.emailPassFormErrors,
    notificationSettings: state.user.notificationSettings,
    emailNotificationFormErrors: state.user.notificationSettings.emailErrors,
  };
}

function mapDispatchToProps(dispatch) {
  return {
    updateUserEmailPass: (formData) => dispatch(updateUserEmailPass(formData)),
    updateUserInfo: (formData) => dispatch(updateUserInfo(formData)),
    updateEmailNotificationSettings: (formData) => dispatch(updateEmailNotificationSettings(formData)),
    fetchEmailNotificationSettings: () => dispatch(fetchEmailNotificationSettings()),
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
    infoFormErrors: React.PropTypes.object.isRequired,
    emailPassFormErrors: React.PropTypes.object.isRequired,
    updateUserInfo: React.PropTypes.func.isRequired,
    updateUserEmailPass: React.PropTypes.func.isRequired,
    // updateUserNotifications: React.PropTypes.func.isRequired,
    fetchEmailNotificationSettings: React.PropTypes.func.isRequired,
    updateEmailNotificationSettings: React.PropTypes.func.isRequired,
    emailNotificationFormErrors: React.PropTypes.array,
  },

  componentWillMount() {
    this.props.fetchEmailNotificationSettings();
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
