"use strict";

var React = require('react');
var Reflux = require('reflux');

var AccountActions = require('../../../actions/account-actions');
var AccountStore = require('../../../stores/account-store');

var SettingsEmailNotifications = require('./settings-email-notifications.jsx');

// TODO: import only things that are used
var _ = require('lodash');


/**
 * Form handling basic user configurations
 * That are email, password and email notifications to get from the site
 */
var SettingsBase = React.createClass({

  mixins: [
    Reflux.connect(AccountStore)
  ],

  componentWillMount: function() {
    AccountActions.userBaseInfo();
  },

  getInitialState: function() {
    return {editMode: false};
  },

  setEditMode: function(event) {
    event.preventDefault();
    this.setState({editMode: true});
  },

  handleSubmit: function(event) {
    event.preventDefault();
    // if the following is success repopulate the user info and set editMode to false
    AccountActions.updateBaseInfo(this.postSubmitted);
  },

  /**
   * When form is submitted, callback this function after the ajax is finished
   * if there ARE errors comming from the backend - don't close the form
   */
  postSubmitted: function() {
    if (_.isEmpty(this.state.userFormErrors)) {
      this.setState({editMode: false});
    } else {
      this.setState({editMode: true});
    }
  },

  /**
   * Show the info (email, password (hidden) and email notifications)
   */
  renderInfo: function() {
    // this.state.user comes from the store that is in the mixin
    // this.state.user may be undefined on initial store config (so we are still loading)
    if (this.state.user !== undefined) {
      return (
        <div className="settings__base">
          <fieldset className="form__fieldset">
            <div className="form-field">
              <label className="form-field__label" htmlFor="username">Username</label>
              <div className="username-display">{ this.state.user.username }</div>
            </div>
            <div className="form-field">
              <label className="form-field__label" htmlFor="username">Email</label>
              <div className="username-display">{ this.state.user.email }</div>
            </div>
            <div className="form-field">
              <label className="form-field__label" htmlFor="username">Pasword</label>
              <div className="username-display">**************</div>
            </div>
          </fieldset>

          <SettingsEmailNotifications
            user={this.state.user}
            editMode={this.state.editMode} />

          <fieldset className="form__fieldset">
            <div className="form-field">
              <div className="form-field__content">
                <a href="#" onClick={ this.setEditMode }>Edit</a>
              </div>
            </div>
          </fieldset>
        </div>
      );
    } else {
      return (
        <div>Loading... (some animation maybe, added as app-action)</div>
      );
    }

  },

  /**
   * If editMode is true, show form from which user can edit base options
   */
  renderForm: function() {
    // this.state.user comes from the store that is in the mixin
    // this.state.user may be undefined on initial store config (so we are still loading)
    if (this.state.user !== undefined) {
      return (
        <form id="base-settings" className="form" method="post" onSubmit={this.handleSubmit}>
          <fieldset className="form__fieldset">
          <input type="hidden" name="username" defaultValue={ this.state.user.username } />

          <div className="form-field">
            <label className="form-field__label" htmlFor="username">Username</label>
            <div className="username-display">{ this.state.user.username }</div>
          </div>

          <div className="form-field">
            <label className="form-field__label" htmlFor="email">Email</label>
            <input className="form-field__text-input" type="email" id="email" name="email" defaultValue={ this.state.user.email } placeholder="i.e. joe@hotmail.com" />

            { this.state.userFormErrors !== undefined && 'email' in this.state.userFormErrors &&
              <div className="form-field-message form-field-message--error form-field-message--settings">
                <h6 className="form-field-message__title">{ this.state.userFormErrors.email.title }</h6>
                <p className="form-field-message__description">{ this.state.userFormErrors.email.description }</p>
              </div>
            }
          </div>

          <div className="form-field">
            <label className="form-field__label" htmlFor="password">Password</label>
            <input className="form-field__password-input" type="password" id="password" name="password" placeholder="********" />

            { this.state.userFormErrors !== undefined && 'password' in this.state.userFormErrors &&
              <div className="form-field-message form-field-message--error form-field-message--settings">
                <h6 className="form-field-message__title">{ this.state.userFormErrors.password.title }</h6>
                <p className="form-field-message__description">{ this.state.userFormErrors.password.message }</p>
              </div>
            }
          </div>

          <div className="form-field">
            <label className="form-field__label" htmlFor="password--confirm">Confirm Password</label>
            <input className="form-field__password-input" type="password" id="password--confirm" name="confirm_password" placeholder="********" />
          </div>

          <SettingsEmailNotifications
            user={this.state.user}
            editMode={this.state.editMode} />

          <input type="submit" className="button--medium" defaultValue="Save" />

          </fieldset>
        </form>
      );
    } else {
      return (
        <div>Loading... (some animation maybe, added as app-action)</div>
      );
    }
  },

  render: function() {
    return (
      <div>
        { this.state.editMode &&
          this.renderForm()
        }

        { !this.state.editMode &&
          this.renderInfo()
        }
      </div>
    );
  }

});


module.exports = SettingsBase;
