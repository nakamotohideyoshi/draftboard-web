import React from 'react';
// import log from '../../../lib/logging';
import forEach from 'lodash/forEach';

/**
 * A form allowing the user to enter their personal details in order to have
 * their identity verified by Trulioo.
 *
 * This is embedded into the deposit page and prevents the user from depositing
 * funds if they do not have a verified identity.
 */
const IdentityForm = React.createClass({
  propTypes: {
    verifyIdentity: React.PropTypes.func.isRequired,
    errors: React.PropTypes.object.isRequired,
    isSending: React.PropTypes.bool.isRequired,
  },


  getDefaultProps() {
    return {
      errors: {},
    };
  },


  onSubmit(event) {
    event.preventDefault();
    this.setState({ values: event.target.value });

    this.props.verifyIdentity({
      first: this.refs.first_name.value,
      last: this.refs.last_name.value,
      birth_day: this.refs.birth_day.value,
      birth_month: this.refs.birth_month.value,
      birth_year: this.refs.birth_year.value,
    });
  },


  renderErrors(errors) {
    const errorList = [];

    forEach(errors, (error, index) => {
      errorList.push(<p key={index} className="form-field-message__description">{ error }</p>);
    });

    if (!errorList.length) {
      return '';
    }

    return (
      <div className="form-field-message form-field-message--error form-field-message--settings">
        { errorList }
      </div>
    );
  },


  renderDateErrors(errors) {
    if (errors.birth_day || errors.birth_month || errors.birth_year) {
      return this.renderErrors(['Enter a valid date.']);
    }

    return '';
  },


  render() {
    return (
      <div className="cmp-identity-form">
        <h3>Account Verification</h3>
        <p>
            Before you can enter contests you need to make a deposit, but first we need to verify
            &nbsp;your account.  Providing the information below helps us prevent fraud and comply
            &nbsp;with state regulations relating to daily fantasy sports.
        </p>
        <div ref="form" className="form">
          <fieldset className="form__fieldset">

            <div className="form-field">
              <label className="form-field__label" htmlFor="first_name">First Name</label>
              <input
                ref="first_name"
                className="form-field__text-input"
                type="text"
                name="first_name"
                required
              />

              {this.renderErrors(this.props.errors.first)}
            </div>

            <div className="form-field">
              <label className="form-field__label" htmlFor="last_name">Last Name</label>
              <input
                ref="last_name"
                className="form-field__text-input"
                type="text"
                name="last_name"
                required
              />

              {this.renderErrors(this.props.errors.last)}
            </div>

            <div className="form-field birth-date">
              <label className="form-field__label" htmlFor="birth_day">Birth Date (M/D/Y)</label>
              <select
                placeholder="Month"
                ref="birth_month"
                className="form-field__select"
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
                className="form-field__text-input"
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
                min="0"
                maxLength="4"
                required
              />

              {this.renderDateErrors(this.props.errors)}
            </div>

            <div className="form-controls">
              <button
                disabled={this.props.isSending}
                ref="submit-button"
                className="button button--flat-alt1"
                onClick={this.onSubmit}
              >Verify Account</button>
            </div>
            <div>
              <a href="/" title="Return to Lobby">Cancel</a>
            </div>
          </fieldset>
        </div>
      </div>
    );
  },
});

module.exports = IdentityForm;
