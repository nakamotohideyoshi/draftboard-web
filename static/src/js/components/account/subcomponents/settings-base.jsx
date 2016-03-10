import React from 'react';
import SettingsEmailNotifications from './settings-email-notifications.jsx';
import isEmpty from 'lodash/lang/isEmpty';


const SettingsBase = React.createClass({

  propTypes: {
    user: React.PropTypes.object.isRequired,
    errors: React.PropTypes.object.isRequired,
    updateUserEmailPass: React.PropTypes.func.isRequired,
    onHandleSubmit: React.PropTypes.func.isRequired,
  },


  getInitialState() {
    return { editMode: false };
  },


  /**
   * if there are no errors coming set edit mode to False
   */
  componentWillReceiveProps(nextProps) {
    if (isEmpty(nextProps.errors)) {
      this.setState({ editMode: false });
    } else {
      this.setState({ editMode: true });
    }
  },


  setEditMode(event) {
    event.preventDefault();
    this.setState({ editMode: true });
  },


  handleSubmit(event) {
    event.preventDefault();
    // get the data from here
    // const email = this.refs.email.value;
    // const password = this.refs.password.value;
    // const passwordConfirm = this.refs.passwordConfirm.value;
    //
    // this.props.updateUserEmailPass({
    //   email,
    //   password,
    //   passwordConfirm,
    // });
  },


  renderInfo() {
    return (
      <div className="settings__base">
        <SettingsEmailNotifications
          user={this.props.user}
          editMode={this.state.editMode}
        />

        <fieldset className="form__fieldset">
          <div className="form-field">
            <div className="form-field__content">
              <a href="#" onClick={ this.setEditMode }>Edit</a>
            </div>
          </div>
        </fieldset>
      </div>
    );
  },


  renderForm() {
    return (
      <form id="base-settings" className="form" method="post" onSubmit={this.handleSubmit}>
        <fieldset className="form__fieldset">
          <SettingsEmailNotifications
            user={this.props.user}
            editMode={this.state.editMode}
          />

          <input type="submit" className="button--medium" defaultValue="Save" />
        </fieldset>
      </form>
    );
  },


  render() {
    return (
      <div>
        { this.state.editMode && this.renderForm() }
        { !this.state.editMode && this.renderInfo() }
      </div>
    );
  },

});


export default SettingsBase;
