import React from 'react';


/**
 * An input form field that handles editing the name of a lineup that's being created.
 */
const DraftNewLineupCardTitle = React.createClass({

  propTypes: {
    title: React.PropTypes.string,
    setTitle: React.PropTypes.func,
  },

  getInitialState() {
    return {
      title: '',
    };
  },


  handleChange(event) {
    this.setState({ title: event.target.value }, () => {
      this.props.setTitle(this.state.title);
    });
  },


  render() {
    return (
      <div className="cmp-lineup-card__title">
        <input
          className="cmp-lineup-card__title-input form-field__text-input"
          value={this.state.title}
          placeholder={this.props.title}
          onChange={this.handleChange}
          maxLength="22"
        />

      </div>
    );
  },

});


module.exports = DraftNewLineupCardTitle;
