import log from '../../lib/logging';
import merge from 'lodash/merge';
import React from 'react';
import renderComponent from '../../lib/render-component';
import { registerUser } from '../../actions/user/register';

// get custom logger for actions
const logComponent = log.getLogger('component');

/*
 * Map Redux actions to React component properties
 * @param  {function} dispatch The dispatch method to pass actions into
 * @return {object}            All of the methods to map to the component, wrapped in 'action' key
 */
export const Register = React.createClass({

  propTypes: {},

  getInitialState() {
    const state = {
      isSubmitting: false,
      fieldNames: [
        'email',
        'username',
        'password',
        'password_confirm',
        'terms',
        'non_field_errors',
      ],
      fields: {},
    };

    state.fieldNames.forEach(name => {
      state.fields[name] = {
        value: '',
        error: null,
      };
    });

    return state;
  },

  resetErrors() {
    const { fieldNames } = this.state;
    const newState = merge({}, this.state);

    fieldNames.forEach(name => {
      newState.fields[name].error = null;
    });
    this.setState(newState);
  },

  handleSubmit(event) {
    event.preventDefault();

    // prevent thrash clicking
    if (this.state.isSubmitting) return false;
    this.setState({ isSubmitting: true });

    this.resetErrors();

    const { email, username, password, password_confirm, terms } = this.refs;

    // have to agree to the terms first
    if (terms.checked === false) {
      this.setState({ terms: { error: true } });
      return false;
    }

    registerUser(
      email.value.toString(),
      username.value.toString(),
      password.value.toString(),
      password_confirm.value.toString()

    // if no redirect and we get here, then use the errors
    ).then(
      // only redirect if success is true, otherwise is error that got caught in action
      response => {
        if (response.success === true) window.location.href = '/contests/';
        return true;
      }).catch(
      // reject = show errors
      errors => {
        logComponent.info('Register.handleSubmit error', errors);

        // if string, then was already taken care of by handleError
        if (typeof errors === 'string') return false;

        const newState = merge({}, this.state);
        Object.keys(errors).forEach(field => {
          if (!(field in newState.fields)) return false;

          newState.fields[field].error = errors[field][0] || null;
          logComponent.warn(errors[field][0]);
        });

        newState.isSubmitting = false;
        this.setState(newState);
      }
    );
  },

  render() {
    const { email, username, password, password_confirm, terms, non_field_errors } = this.state.fields;
    let nonFieldErrors;

    if (non_field_errors.error !== null) {
      nonFieldErrors = (
        <div className="account__left__content__form__non-field-errors">
          {non_field_errors.error}
        </div>
      );
    }

    return (
      <form className="account__left__content__form" method="post" onSubmit={this.handleSubmit}>
        {nonFieldErrors}

        <div className={`account__left__content__form__input-layout ${(email.error) ? 'errored' : ''}`}>
          <label htmlFor="email">
            Email <span>{(email.error) ? `- ${email.error}` : ''}</span>
          </label>
          <input ref="email" id="email" type="text" name="email" defaultValue={email.value} required />
        </div>

        <div className={`account__left__content__form__input-layout ${(username.error) ? 'errored' : ''}`}>
          <label htmlFor="username">
            Username <span>{(username.error) ? `- ${username.error}` : ''}</span>
          </label>
          <input ref="username" id="username" type="text" name="username" defaultValue={username.value} required />
        </div>

        <div className={`account__left__content__form__input-layout ${(password.error) ? 'errored' : ''}`}>
          <label htmlFor="password">
            Password <span>{(password.error) ? `- ${password.error}` : ''}</span>
          </label>
          <input ref="password" id="password" type="password" name="password" required />
        </div>

        <div className={`account__left__content__form__input-layout ${(password_confirm.error) ? 'errored' : ''}`}>
          <label htmlFor="password_confirm">
            Confirm password <span>{(password_confirm.error) ? `- ${password_confirm.error}` : ''}</span>
          </label>
          <input ref="password_confirm" id="password_confirm" type="password" name="password_confirm" required />
        </div>

        <div
          className={`account__left__content__form__input-layout__terms \
            account__left__content__form__input-layout ${(terms.error) ? 'errored' : ''}`}
        >
          <input ref="terms" name="terms" type="checkbox" value="terms" required />
          <p>
            I am at least 18 years or older and accept the
            <a href="/terms-conditions/" target="_blank">Terms &amp; Agreement.</a>
          </p>
        </div>

        <div className="account__left__content__form__input-layout">
          <input type="submit" value="Create account" />
          <span className="arrow"></span>
        </div>
      </form>
    );
  },

});


renderComponent(
  <Register />,
  '#account-register'
);
