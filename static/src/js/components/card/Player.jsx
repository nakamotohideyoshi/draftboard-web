import React, { Component } from 'react';
import PropTypes from 'prop-types';

class Player extends Component {
  componentWillMount() {
    const cost = `$${this.props.cost}`;

    this.setState(
      {
        cost,
        active: false,
      }
    );
  }
  getCost(cost) {
    if (!cost) {
      return null;
    }

    return (
      <h4>{ this.state.cost }</h4>
    );
  }
  getMeta(meta) {
    if (!meta) {
      return null;
    }

    return (
      <p className="meta">
        { this.props.meta}
      </p>
    );
  }
  doStuff() {
    if (this.state.active === 'active') {
      this.setState({ active: 'inactive' });
    } else {
      this.setState({ active: 'active' });
    }
  }
  render() {
    return (
      <div
        onClick={this.doStuff.bind(this)}
        className={`${this.state.active} ${this.props.classes} player player-grid v-align-center`}
      >
        <h6 className="position grid-col-1 center-align">{ this.props.position }</h6>

        <div className="effect-circle grid-col-1 center-align">
          <span className="image" style={{ backgroundImage: `url(${this.props.image})` }}></span>
        </div>

        <div className="info grid-col-6">
          <p className="name">{ this.props.name }</p>
          { this.getMeta(this.props.meta) }
        </div>

        <div className="score grid-col-1 right-align">
          { this.getCost(this.props.cost) }
          <h5>{ this.props.ffpg }</h5>
        </div>
        <div className="grid-col-9">
          {this.props.children}
        </div>
      </div>
    );
  }
}

Player.propTypes = {
  image: PropTypes.string,
  children: PropTypes.element,
  position: PropTypes.string,
  name: PropTypes.string,
  team: PropTypes.string,
  meta: PropTypes.object,
  ffpg: PropTypes.number,
  cost: PropTypes.func,
  classes: PropTypes.string,
};


export default Player;
