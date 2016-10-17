import React from 'react';
import log from '../../../lib/logging';


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
  },


  getDefaultProps() {
    return {
      errors: {},
    };
  },


  onSubmit(event) {
    event.preventDefault();
    log.info(event);
    this.setState({ values: event.target.value });

    this.props.verifyIdentity({
      first: this.refs.first_name.value,
      last: this.refs.last_name.value,
      birth_day: this.refs.birth_day.value,
      birth_month: this.refs.birth_month.value,
      birth_year: this.refs.birth_year.value,
      postal_code: this.refs.postal_code.value,
    });
  },


  renderErrors() {
    return '';
  },


  render() {
    return (
      <div className="cmp-identity-form">
        <form ref="form" className="form">
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

              {this.renderErrors(this.props.errors.first_name)}
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

              {this.renderErrors(this.props.errors.last_name)}
            </div>

            <div className="form-field birth-date">
              <label className="form-field__label" htmlFor="birth_day">Birth Date (D/M/Y)</label>
              <input
                placeholder="D"
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
                placeholder="M"
                ref="birth_month"
                className="form-field__text-input"
                type="number"
                name="birth_month"
                min="1"
                max="12"
                required
              />
              /
              <input
                placeholder="Y"
                ref="birth_year"
                className="form-field__text-input"
                type="number"
                name="birth_year"
                max="9999"
                min="0"
                maxLength="4"
                required
              />

              {this.renderErrors(this.props.errors.last_name)}
            </div>

            <div className="form-field">
              <label className="form-field__label" htmlFor="postal_code">Postal Code</label>
              <input
                ref="postal_code"
                className="form-field__text-input"
                type="text"
                name="postal_code"
                required
              />

              {this.renderErrors(this.props.errors.postal_code)}
            </div>

            <button
              ref="submit-button"
              className="button button--flat-alt1"
              onClick={this.onSubmit}
            >Submit</button>

          </fieldset>
        </form>
      </div>
    );
  },
});

module.exports = IdentityForm;
