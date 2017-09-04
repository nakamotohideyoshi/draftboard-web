import React from 'react';
import moment from 'moment';
import PropTypes from 'prop-types';
// import log from '../../lib/logging';

class CardFooter extends React.Component {
  componentWillMount() {
    this.setState(
      {
        timer: null,
        secondsElapsed: 0,
      }
    );
  }

  componentDidMount() {
    if (this.props.start) {
      this.startGameTimer(this.props.start);
    }
  }
  componentWillReceiveProps(nextProps) {
    if (nextProps.start !== this.props.start) {
      this.startGameTimer(nextProps.start);
    }
  }
  // timer cleanup
  componentWillUnmount() {
    if (this.state.timer !== null) {
      window.clearInterval(this.state.timer);
    }
  }
  // this can be abstracted into
  // libs making this all much cleaner
  getRemainingTime(timestamp) {
    const eventTime = moment.utc(timestamp);
    const currentTime = moment(new Date().getTime()).utc();
    const diffTime = eventTime - currentTime;
    const durationhours = Math.floor(moment.duration(diffTime).asHours());
    const durationminutes = moment.duration(diffTime).minutes();
    const durartionseconds = moment.duration(diffTime).seconds();
    const dateobj = {};

    if (diffTime > 0) {
      dateobj.hours = durationhours < 10 ? `0${durationhours}` : durationhours;
      dateobj.minutes = durationminutes < 10 ? `0${durationminutes}` : durationminutes;
      dateobj.seconds = durartionseconds < 10 ? `0${durartionseconds}` : durartionseconds;
    } else {
      dateobj.hours = '00';
      dateobj.minutes = '00';
      dateobj.seconds = '00';
    }

    return dateobj;
  }

  getFooterLabels(key) {
    let label;

    switch (key) {
      case 'playeravg':
        label = 'Player / Avg';
        break;
      case 'remsalary':
        label = 'Rem Salary';
        break;
      case 'start':
        label = 'Live In';
        break;
      default:
        label = key;
        break;
    }

    return label;
  }

  getFooterItems() {
    const footerItems = [];

    for (const key in this.props) {
      if (this.props.hasOwnProperty(key)) {
        const item = key;
        let value = this.props[key];
        const isneg = parseInt(value, 10) < 0 && item !== 'start' ? 'negative' : '';

        // preformat time remaining
        if (item === 'start') {
          const remaining = this.getRemainingTime(value);
          value = this.formatClock(remaining);
        }

        // add $ sign if its needed
        if (
          item === 'remsalary' ||
          item === 'fees' ||
          item === 'playeravg') {
          value = `$${value}`;
        }

        if (item !== 'children') {
          footerItems.push([
            <dd key={item} className={`card-${item}`}>
              <dl>
                <dt>{this.getFooterLabels(item)}</dt>
                <dd ref={key} className={ isneg } >{value}</dd>
              </dl>
            </dd>,
          ]);
        }
      }
    }

    return footerItems;
  }

  startGameTimer(timestamp) {
    const timer = window.setInterval(() => {
      const remaining = this.getRemainingTime(timestamp);

      this.refs.hours.textContent = remaining.hours;
      this.refs.minutes.textContent = remaining.minutes;
      this.refs.seconds.textContent = remaining.seconds;

      this.setState({ secondsElapsed: this.state.secondsElapsed + 1 });
    }, 1000);

    this.setState({ timer });
  }

  formatClock(time) {
    return (
      <span className="clock">
        <span className="hours" ref="hours">{time.hours}</span>
        <span>:</span>
        <span className="minutes" ref="minutes">{time.minutes}</span>
        <span>:</span>
        <span className="seconds" ref="seconds">{time.seconds}</span>
      </span>
    );
  }

  render() {
    return (
      <footer>
        <dl>
          {this.getFooterItems()}
        </dl>
        {this.props.children}
      </footer>
    );
  }
}

CardFooter.propTypes = {
  children: PropTypes.element,
  fees: PropTypes.number,
  entries: PropTypes.number,
  start: PropTypes.string,
  playeravg: PropTypes.string,
  remsalary: PropTypes.string,
};

export default CardFooter;
