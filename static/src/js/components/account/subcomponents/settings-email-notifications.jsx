import React from 'react';
import { isEmpty as _isEmpty } from 'lodash';
import { forEach as _forEach } from 'lodash';

const SettingsEmailNotifications = React.createClass({

  propTypes: {
    user: React.PropTypes.object.isRequired,
    errors: React.PropTypes.array.isRequired,
    handleSubmit: React.PropTypes.func.isRequired,
    emailNotificationSettings: React.PropTypes.array.isRequired,
    isUpdatingEmail: React.PropTypes.bool,
    isFetchingEmail: React.PropTypes.bool,
  },


  getInitialState() {
    return {
      editMode: false,
      user: this.props.user,
    };
  },


  /**
   * if there are no errors comming set edit mode to False
   */
  componentWillReceiveProps(nextProps) {
    if (_isEmpty(nextProps.errors) || nextProps.isUpdatingEmail) {
      this.setState({ editMode: false });
    } else {
      this.setState({ editMode: true });
    }

    // Update user info.
    if (!Object.keys(this.state.user).length) {
      this.setState({ user: nextProps.user });
    }
  },


  setEditMode(event) {
    event.preventDefault();
    this.setState({ editMode: true });
  },


  handleSubmit() {
    const fieldset = this.refs.formFieldset;
    if (fieldset) {
      const values = [];

      _forEach(fieldset.querySelectorAll('input'), (field) => {
        if (field.checked) {
          values.push({
            id: field.getAttribute('data-notification-id'),
            enabled: field.value,
          });
        }
      });

      this.props.handleSubmit(values);
    }
  },


  renderInfo() {
    const notificationList = this.props.emailNotificationSettings.map((notification) =>
      <li key={notification.notification_info.name}>
        {notification.notification_info.description}
      </li>
    );

    return (
      <div className="info-state">
        <ul>
          {notificationList}
        </ul>

        <a href="#" onClick={this.setEditMode}>Edit</a>
      </div>
    );
  },


  renderErrors() {
    if (this.props.errors) {
      return (
        <div className="error"><p>{this.props.errors}</p></div>
      );
    }

    return (<div></div>);
  },


  renderSaveButton() {
    if (this.props.isUpdatingEmail) {
      return (
        <input
          type="submit"
          className="button--medium"
          defaultValue="Saving..."
        />
      );
    }

    return (
      <input
        type="submit"
        className="button--medium"
        defaultValue="Save"
        onClick={this.handleSubmit}
      />
    );
  },


  renderForm() {
    const notificationList = this.props.emailNotificationSettings.map((notification) =>
      <li key={notification.notification_info.name}>
        <div>
          <div className="radio-button-list__title">
            {notification.notification_info.description}
          </div>

          <div className="radio-button-list__button-container pull-right">
            <input
              className="radio-button-list__input"
              data-notification-id={notification.notification_info.id}
              type="radio"
              id={`${notification.notification_info.name}--off`}
              name={`${notification.notification_info.name}`}
              value="false"
              defaultChecked={!notification.enabled}
            />
            <label
              className="radio-button-list__label"
              htmlFor={`${notification.notification_info.name}--off`}
            >Off</label>
          </div>

          <div className="radio-button-list__button-container pull-right">
            <input
              className="radio-button-list__input"
              data-notification-id={notification.notification_info.id}
              type="radio"
              id={`${notification.notification_info.name}--on`}
              name={`${notification.notification_info.name}`}
              value="true"
              defaultChecked={notification.enabled}
            />
            <label
              className="radio-button-list__label"
              htmlFor={`${notification.notification_info.name}--on`}
            >On</label>
          </div>
        </div>
      </li>
    );


    return (
      <div className="edit-state">
        <ul className="radio-button-list">
          <li>
            <div className="radio-button-list__header-label">Off</div>
            <div className="radio-button-list__header-label">On</div>
          </li>

          {notificationList}
        </ul>

        {this.renderErrors()}

        {this.renderSaveButton()}
      </div>
    );
  },

  render() {
    return (
      <form className="cmp-settings-email-notifications">
        <fieldset className="form__fieldset" ref="formFieldset">
          <div className="form-field form-field--with-help">
            <label className="form-field__label" htmlFor="notifications">Email Notifications</label>

            <div className="form-field__content">
              <p className="form-field__info">
                Here you can change your email notication preferences.
              </p>

              { this.state.editMode && this.renderForm() }
              { !this.state.editMode && this.renderInfo() }
            </div>
          </div>
        </fieldset>
      </form>
    );
  },

});


export default SettingsEmailNotifications;
