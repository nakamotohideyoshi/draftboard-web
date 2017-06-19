import log from '../../lib/logging';
import { querystring } from '../../lib/utils';
import merge from 'lodash/merge';
import React from 'react';
import renderComponent from '../../lib/render-component';
import RegisterConfirmModal from './register-confirm-modal';
import { registerUser } from '../../actions/user/register';
import {
  isListOfErrors,
  // isFieldValidationErrorObject,
  isRawTextError,
  isExceptionDetail,
} from '../../lib/utils/response-types';

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
        'first',
        'last',
        'username',
        'email',
        'password',
        // 'password_confirm',
        'non_field_errors',
        'birth_day',
        'birth_month',
        'birth_year',
        'postal_code',
      ],
      fields: {},
      nonFieldErrors: [],

      errors: {},
      signup_anyway: false,
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
    newState.nonFieldErrors = [];
    this.setState(newState);
  },

  handleSubmit(event) {
    if (event) event.preventDefault();
    // prevent thrash clicking
    if (this.state.isSubmitting) return false;
    this.resetErrors();
    this.setState({ isSubmitting: true });

    registerUser(
      this.refs.first.value.toString(),
      this.refs.last.value.toString(),
      this.refs.birth_day.value.toString(),
      this.refs.birth_month.value.toString(),
      this.refs.birth_year.value.toString(),
      this.refs.postal_code.value.toString(),
      this.refs.email.value.toString(),
      this.refs.username.value.toString(),
      this.refs.password.value.toString(),
      this.state.signup_anyway
    // if no redirect and we get here, then use the errors
    ).then(
      // only redirect if success is true, otherwise is error that got caught in action
      response => {
        if (response.success === true) {
          const qs = querystring();
          // If we have a `?next=` in the url, go to there, otherwise
          // redirect to the lobby.
          window.location.href = qs.next || '/contests/';
        }
        return true;
      }).catch(
      // reject = show errors
      errors => {
        logComponent.info('Register.handleSubmit error', errors);

        // clear old errors
        this.setState({
          errors: {},
        });

        // if string, then was already taken care of by handleError
        if (isRawTextError({ body: errors })) return false;

        if (isExceptionDetail({ body: errors })) {
          this.setState({ nonFieldErrors: [errors.detail] });
        }

        if (isListOfErrors({ body: errors })) {
          this.setState({ nonFieldErrors: errors });
        }

        this.setState({
          errors,
          isSubmitting: false,
        }, () => {
          const newState = merge({}, this.state);

          Object.keys(errors).forEach(field => {
            if (!(field in newState.fields)) return false;

            newState.fields[field].error = errors[field][0] || null;
            logComponent.warn(errors[field][0]);
          });

          newState.isSubmitting = false;
          this.setState(newState);
        });
      }
    );
  },

  // When the user clicks the 'SIGN UP' button.
  handleModalConfirmEntry() {
    // Hide modal
    this.setState({
      signup_anyway: true,
      errors: {},
    }, this.handleSubmit); // Send req again
  },

  // When the user clicks the 'NO THANKS' button.
  handleModalCancelEntry() {
    window.location.href = '/'; // Redirect to main page
  },


  renderDateErrors() {
    const fields = this.state.fields;

    if (fields.birth_day.error || fields.birth_month.error || fields.birth_year.error) {
      return (
        <div className="account__left__content__form__non-field-errors">
          <span>{(fields.birth_day.error) ? `Birth Day - ${fields.birth_day.error}` : ''}</span>
          <span>{(fields.birth_month.error) ? `Birth Month - ${fields.birth_month.error}` : ''}</span>
          <span>{(fields.birth_year.error) ? `Birth Year - ${fields.birth_year.error}` : ''}</span>
        </div>
      );
    }

    return <div></div>;
  },


  /**
   * Renders any non field-specific errors into divs.
   * @param nonFieldErrors
   * @returns {XML}
   */
  renderNonFieldErrors() {
    const combinedErrors = [].concat(this.state.fields.non_field_errors.error || []).concat(this.state.nonFieldErrors);

    const errors = combinedErrors.map((error, i) => (
        <div key={i}>{error}</div>
    ));

    if (!errors.length) {
      return <div></div>;
    }

    return (
      <div className="account__left__content__form__non-field-errors">
        {errors}
      </div>
    );
  },


  render() {
    const { first, last, postal_code, email, username, password } = this.state.fields;

    let submitClasses = 'button button--gradient';
    if (this.state.isSubmitting) {
      submitClasses += ' button--disabled';
    }


    return (
      <form className="account__left__content__form" method="post" onSubmit={this.handleSubmit}>

        <div className="split_field_group">
          <div
            className={`account__left__content__form__input-layout ${(first.error) ? 'errored' : ''}`}
          >
            <label htmlFor="password">
              First Name <span>{(first.error) ? `- ${first.error}` : ''}</span>
            </label>
            <input ref="first" id="first" type="text" name="first" required />
          </div>

          <div className={
            `account__left__content__form__input-layout ${(last.error) ? 'errored' : ''}`}
          >
            <label htmlFor="password">
              Last Name <span>{(last.error) ? `- ${last.error}` : ''}</span>
            </label>
            <input ref="last" id="last" type="text" name="last" required />
          </div>
        </div>

        <div className={
          `account__left__content__form__input-layout ${(username.error) ? 'errored' : ''}`}
        >
          <label htmlFor="username">
            Username <span>{(username.error) ? `- ${username.error}` : ''}</span>
          </label>
          <input
            ref="username" id="username"
            type="text" name="username" defaultValue={username.value} required
          />
        </div>

        <div className={
          `account__left__content__form__input-layout ${(email.error) ? 'errored' : ''}`}
        >
          <label htmlFor="email">
            Email <span>{(email.error) ? `- ${email.error}` : ''}</span>
          </label>
          <input ref="email" id="email" type="text" name="email" defaultValue={email.value} required />
        </div>

        <div className={
          `account__left__content__form__input-layout ${(password.error) ? 'errored' : ''}`}
        >
          <label htmlFor="password">
            Password <span>{(password.error) ? `- ${password.error}` : ''}</span>
          </label>
          <input ref="password" id="password" type="password" name="password" required />
        </div>

        <div
          className="account__left__content__form__input-layout birth-date"
        >
          <label htmlFor="birth_day">
            Birth Date (M/D/Y)
            {this.renderDateErrors()}
          </label>
          <select
            placeholder="Month"
            ref="birth_month"
            className="form-field__select birth-month"
            type="number"
            name="birth_month"
            min="1"
            max="12"
            required
          >
            <option value="01">Jan</option>
            <option value="02">Feb</option>
            <option value="03">Mar</option>
            <option value="04">Apr</option>
            <option value="05">May</option>
            <option value="06">Jun</option>
            <option value="07">Jul</option>
            <option value="08">Aug</option>
            <option value="09">Sep</option>
            <option value="10">Oct</option>
            <option value="11">Nov</option>
            <option value="12">Dec</option>
          </select>
          /
          <input
            placeholder="DD"
            ref="birth_day"
            className="form-field__text-input birth-day"
            type="number"
            name="birth_day"
            min="1"
            max="31"
            required
          />
          /
          <input
            placeholder="YYYY"
            ref="birth_year"
            className="form-field__text-input birth-year"
            type="number"
            name="birth_year"
            max="9999"
            min="1912"
            maxLength="4"
            required
          />
        </div>

        <div className={`account__left__content__form__input-layout ${(postal_code.error) ? 'errored' : ''}`}>
          <label htmlFor="postal_code">
            Postal Code <span>{(postal_code.error) ? `- ${postal_code.error}` : ''}</span>
          </label>
          <input ref="postal_code" id="postal_code" type="text" name="postal_code" required />
        </div>

        {this.renderNonFieldErrors(this.state.nonFieldErrors)}

        <div className="account__left__content__form__input-layout">
          <input type="submit" value="Create account" className={submitClasses} />

          <RegisterConfirmModal
            isOpen={this.state.errors.verification_modal}
            confirmEntry={this.handleModalConfirmEntry}
            cancelEntry={this.handleModalCancelEntry}
            titleText={this.state.errors.title}
          >
            {this.state.errors.message}
          </RegisterConfirmModal>

          <span className="arrow" />
          <p>Clicking "Confirm" is an agreement to our <a href="/terms-conditions/" target="_blank">
            Terms of Use</a> and <a href="/privacy-policy/" target="_blank">Privacy Policy</a></p>
        </div>
      </form>
    );
  },

});


renderComponent(
  <Register />,
  '#account-register'
);
