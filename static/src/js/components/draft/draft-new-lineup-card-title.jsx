'use strict';

var React = require('react');


/**
 * An input form field that handles editing the name of a lineup that's being created.
 */
var DraftNewLineupCardTitle = React.createClass({

  propTypes: {
    title: React.PropTypes.string,
    setTitle: React.PropTypes.func
  },

  getInitialState: function() {
    return {
      title: ''
    };
  },


  handleChange: function(event) {
    this.setState({title: event.target.value}, function() {
      this.props.setTitle(this.state.title);
    });
  },


  render: function() {

    // var renderVal = this.state.title;
    //
    // if (this.state.title === this.props.title) {
    //   renderVal = '';
    // }

    return (
      <div className="cmp-lineup-card__title">

        <input
          className="cmp-lineup-card__title-input form-field__text-input"
          value={this.state.title}
          placeholder={this.props.title}
          onChange={this.handleChange}
        />

      </div>
    );
  }

});


module.exports = DraftNewLineupCardTitle;
