import React from 'react';

/**
 * Renders a user's Identity Information (name, dob, postal code).
 */
const Identity = (props) => {
  if (!props.identity || Object.keys(props.identity).length === 0) {
    return (
      <div className="cmp-account-identity">
        <fieldset className="form__fieldset">
          <p>No Identity Information Found</p>
        </fieldset>
      </div>
    );
  }

  return (
    <div className="cmp-identity">
      <fieldset className="form__fieldset">
        <div className="form-field">
          <label className="form-field__label">Name</label>
          <div className="username-display">
            {props.identity.first_name} {props.identity.last_name}
          </div>
        </div>
        <div className="form-field">
          <label className="form-field__label">Birth Date (D/M/Y)</label>
          <div className="dob-display">
            {props.identity.birth_day}/{props.identity.birth_month}/{props.identity.birth_year}
          </div>
        </div>
        <div className="form-field">
          <label className="form-field__label">Postal Code</label>
          <div className="postal_code-display">{props.identity.postal_code}</div>
        </div>
        <p><em>To change this information, contact support@draftboard.com</em></p>
      </fieldset>
    </div>
  );
};

Identity.propTypes = {
  identity: React.PropTypes.object,
};

export default Identity;
