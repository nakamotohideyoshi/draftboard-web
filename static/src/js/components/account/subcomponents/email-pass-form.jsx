import React from 'react';
import isEmpty from 'lodash/lang/isEmpty';


const EmailPasssForm = React.createClass({

  propTypes: {
    username: React.PropTypes.string.isRequired,
    user: React.PropTypes.object.isRequired,
    errors: React.PropTypes.object.isRequired,
    updateUserEmailPass: React.PropTypes.func.isRequired,
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
    const email = this.refs.email.value;
    const password = this.refs.password.value;
    const passwordConfirm = this.refs.passwordConfirm.value;

    this.props.updateUserEmailPass({
      email,
      password,
      passwordConfirm,
    });
  },

  renderInfo() {
    return (
      <div className="settings__base">
        <fieldset className="form__fieldset">
          <div className="form-field">
            <label className="form-field__label" htmlFor="username">Username</label>
            <div className="username-display">{ this.props.username }</div>
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
    let emailClasses = 'email' in this.props.errors ? 'form-field--error ' : '';
    emailClasses += 'form-field';

    let passwordClasses = 'password' in this.props.errors ? 'form-field--error ' : '';
    passwordClasses += 'form-field';

    return (
      <form id="base-settings" className="form" method="post" onSubmit={this.handleSubmit}>
        <fieldset className="form__fieldset">
        <input type="hidden" name="username" defaultValue={ this.props.username } />

        <div className="form-field">
          <label className="form-field__label" htmlFor="username">Username</label>
          <div className="username-display">{ this.props.username }</div>
        </div>

        <div className={emailClasses}>
          <label className="form-field__label" htmlFor="email">Email</label>
          <input
            ref="email"
            className="form-field__text-input"
            type="email"
            id="email"
            name="email"
            defaultValue={ this.props.user.email }
            placeholder="i.e. joe@hotmail.com"
          />

          { 'email' in this.props.errors &&
            <div className="form-field-message form-field-message--error form-field-message--settings">
              <p className="form-field-message__description">{ this.props.errors.email.description }</p>
            </div>
          }
        </div>

        <div className={passwordClasses}>
          <label className="form-field__label" htmlFor="password">Password</label>
          <input
            ref="password"
            className="form-field__password-input"
            type="password"
            id="password"
            name="password"
            placeholder="********"
          />

          { 'password' in this.props.errors &&
            <div className="form-field-message form-field-message--error form-field-message--settings">
              <p className="form-field-message__description">{ this.props.errors.password.description }</p>
            </div>
          }
          </div>

        <div className="form-field">
          <label className="form-field__label" htmlFor="password--confirm">Confirm Password</label>
          <input
            ref="passwordConfirm"
            className="form-field__password-input"
            type="password"
            id="password--confirm"
            name="confirm_password"
            placeholder="********"
          />
        </div>

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


export default EmailPasssForm;
