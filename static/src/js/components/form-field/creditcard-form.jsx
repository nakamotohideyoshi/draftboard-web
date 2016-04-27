import React from 'react';
import ReactCardFormContainer from 'card-react';


const CreditcardForm = React.createClass({
  newPaymentMethod(event) {
    event.preventDefault();
  },

  render() {
    return (
      <ReactCardFormContainer

        container="react-credit-card-animator"

        formInputsNames={
        {
          number: 'CCnumber',
          expiry: 'CCexpiry',
          cvc: 'CCcvc',
          name: 'CCname',
        }
        }
      >

        <div id="react-credit-card-animator" />

        <form className="form form--credit_card_input" onSubmit={this.newPaymentMethod}>
          <div className="form-field">
            <label className="form-field__label" htmlFor="CCnumber">Card number</label>
            <input className="form-field__text-input" type="text" name="CCnumber" id="CCnumber" />
          </div>

          <div className="form-field">
            <label className="form-field__label" htmlFor="CCname">Cardholders name</label>
            <input className="form-field__text-input" type="text" name="CCname" id="CCname" />
          </div>

          <div className="form-field">
            <label className="form-field__label" htmlFor="CCexpiry">Expiry Date</label>
            <input className="form-field__text-input" type="text" name="CCexpiry" id="CCexpiry" />
          </div>

          <div className="form-field">
            <label className="form-field__label" htmlFor="CCcvc">CVV Code</label>
            <input className="form-field__text-input" type="text" name="CCcvc" id="CCcvc" />
          </div>

          <input type="submit" className="button button--flat-alt1" value="ADD CARD" />
        </form>

      </ReactCardFormContainer>
    );
  },

});


export default CreditcardForm;
