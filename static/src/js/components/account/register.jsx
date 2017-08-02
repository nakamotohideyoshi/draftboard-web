import log from '../../lib/logging';
import * as ReactRedux from 'react-redux';
import { querystring } from '../../lib/utils';
import merge from 'lodash/merge';
import React from 'react';
import store from '../../store';
import renderComponent from '../../lib/render-component';
import RestrictedLocationConfirmModal from './restricted-location-confirm-modal';
import { verifyLocation } from '../../actions/user';
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
function mapDispatchToProps(dispatch) {
  return {
    verifyLocation: () => dispatch(verifyLocation()),
  };
}

function mapStateToProps(state) {
  return {
    userLocation: state.user.location,
  };
}

export const Register = React.createClass({

  propTypes: {
    verifyLocation: React.PropTypes.func.isRequired,
    userLocation: React.PropTypes.object.isRequired,
  },


  getInitialState() {
    const state = {
      isSubmitting: false,
      fieldNames: [
        'username',
        'email',
        'password',
        // 'password_confirm',
        'non_field_errors',
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


  componentWillMount() {
    // When we first boot up this component, fire off a request to
    // check if the user is in a valid location. If they are not,
    // we will use props.userLocation to signal the component to
    // show a confirmation modal.
    this.props.verifyLocation();
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
      this.refs.username.value.toString(),
      this.refs.email.value.toString(),
      this.refs.password.value.toString()
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

  renderLocationConfirmModalIfNeeded() {
    // If we know that they are in a blocked location because we have checked.
    if (
      this.props.userLocation.hasAttemptedToVerify &&
      !this.props.userLocation.isLocationVerified
    ) {
      // Show a modal warning them that they will not be able to do some things.
      return (
          <RestrictedLocationConfirmModal
            isOpen
            titleText="Location Unavailable"
            continueButtonText="Sign Up"
          >
            <div>{this.props.userLocation.message || 'Your location could not be verified.'}</div>
          </RestrictedLocationConfirmModal>
      );
    }
    // By default do not show confirm modal.
    return '';
  },

  render() {
    const { email, username, password } = this.state.fields;
    let submitClasses = 'button button--gradient button--tall';

    if (this.state.isSubmitting) {
      submitClasses += ' button--disabled';
    }

    return (
      <form className="account__left__content__form" method="post" onSubmit={this.handleSubmit}>

        <div className={
          `account__left__content__form__input-layout ${(email.error) ? 'errored' : ''}`}
        >
          <label htmlFor="email">
            Email <span>{(email.error) ? `- ${email.error}` : ''}</span>
          </label>
          <input
            ref="email"
            id="email"
            type="text"
            name="email"
            defaultValue={email.value}
            placeholder="user@email.com"
            required
          />
        </div>

        <div className={
          `account__left__content__form__input-layout ${(username.error) ? 'errored' : ''}`}
        >
          <label htmlFor="username">
            Username <span>{(username.error) ? `- ${username.error}` : ''}</span>
          </label>
          <input
            ref="username"
            id="username"
            type="text"
            name="username"
            defaultValue={username.value}
            placeholder="How you will appear to others"
            required
          />
        </div>

        <div className={
          `account__left__content__form__input-layout ${(password.error) ? 'errored' : ''}`}
        >
          <label htmlFor="password">
            Password <span>{(password.error) ? `- ${password.error}` : ''}</span>
          </label>
          <input
            ref="password"
            id="password"
            type="password"
            name="password"
            placeholder="Must be at least 8 characters"
            required
          />
        </div>

        {this.renderNonFieldErrors()}

        <div className="account__left__content__form__input-layout">
          <button className={submitClasses}>Create Account <span className="right">→</span></button>
          <p>
            Clicking "Create Account" confirms you’re 18+ (19+ in NE, 21+ in MA) and agree to our
             &nbsp;<a href="/terms-conditions/" target="_blank">Terms</a> and
             &nbsp;<a href="/privacy-policy/" target="_blank">Privacy Policy</a>.
          </p>
        </div>

        {this.renderLocationConfirmModalIfNeeded()}
      </form>
    );
  },

});


// Set up Redux connections to React
const { Provider, connect } = ReactRedux;


// Wrap the component to inject dispatch and selected state into it.
const RegisterConnected = connect(
  mapStateToProps,
  mapDispatchToProps
)(Register);


renderComponent(
  <Provider store={store}>
    <RegisterConnected />
  </Provider>,
  '#account-register'
);
