'use strict';

import React from 'react';

const SettingsEmailNotifications = require('./settings-email-notifications.jsx');
const isEmpty = require('lodash/lang/isEmpty');


const SettingsBase = React.createClass({

  propTypes: {
    user: React.PropTypes.object.isRequired,
    errors: React.PropTypes.object.isRequired,
    onHandleSubmit: React.PropTypes.func.isRequired
  },

  getInitialState() {
    return {editMode: false}
  },

  /**
   * if there are no errors comming set edit mode to False
   */
  componentWillReceiveProps(nextProps) {
    if (isEmpty(nextProps.errors)) {
      this.setState({editMode: false})
    } else {
      this.setState({editMode: true})
    }
  },

  setEditMode(event) {
    event.preventDefault();
    this.setState({editMode: true});
  },

  handleSubmit(event) {
    event.preventDefault();
    // get the data from here
    this.props.onHandleSubmit({});
  },

  renderInfo() {
    return (
      <div className="settings__base">
        <fieldset className="form__fieldset">
          <div className="form-field">
            <label className="form-field__label" htmlFor="username">Username</label>
            <div className="username-display">{ this.props.user.username }</div>
          </div>
          <div className="form-field">
            <label className="form-field__label" htmlFor="username">Email</label>
            <div className="username-display">{ this.props.user.email }</div>
          </div>
          <div className="form-field">
            <label className="form-field__label" htmlFor="username">Pasword</label>
            <div className="username-display">**************</div>
          </div>
        </fieldset>

        <SettingsEmailNotifications
          user={this.props.user}
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
  },

  renderForm() {
    return (
      <form id="base-settings" className="form" method="post" onSubmit={this.handleSubmit}>
        <fieldset className="form__fieldset">
        <input type="hidden" name="username" defaultValue={ this.props.user.username } />

        <div className="form-field">
          <label className="form-field__label" htmlFor="username">Username</label>
          <div className="username-display">{ this.props.user.username }</div>
        </div>

        <div className="form-field">
          <label className="form-field__label" htmlFor="email">Email</label>
          <input className="form-field__text-input" type="email" id="email" name="email" defaultValue={ this.props.user.email } placeholder="i.e. joe@hotmail.com" />

          { 'email' in this.props.errors &&
            <div className="form-field-message form-field-message--error form-field-message--settings">
              <h6 className="form-field-message__title">{ this.props.errors.email.title }</h6>
              <p className="form-field-message__description">{ this.props.errors.email.description }</p>
            </div>
          }
        </div>

        <div className="form-field">
          <label className="form-field__label" htmlFor="password">Password</label>
          <input className="form-field__password-input" type="password" id="password" name="password" placeholder="********" />

          { 'password' in this.props.errors &&
            <div className="form-field-message form-field-message--error form-field-message--settings">
              <h6 className="form-field-message__title">{ this.props.errors.password.title }</h6>
              <p className="form-field-message__description">{ this.props.errors.password.message }</p>
            </div>
          }
          </div>

        <div className="form-field">
          <label className="form-field__label" htmlFor="password--confirm">Confirm Password</label>
          <input className="form-field__password-input" type="password" id="password--confirm" name="confirm_password" placeholder="********" />
        </div>

        <SettingsEmailNotifications
          user={this.props.user}
          editMode={this.state.editMode} />

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
  }

});


export default SettingsBase;
