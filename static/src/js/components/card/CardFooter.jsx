import React from 'react';
import moment from 'moment';
import PropTypes from 'prop-types';
import log from '../../lib/logging';

class CardFooter extends React.Component {
  componentDidMount() {
    this.setState({ timer: null });
    if (this.props.start) {
      this.startGameTimer(this.props.start);
    }
  }

  // timer cleanup
  componentWillUnmount() {
    if (this.state.timer !== null) {
      clearInterval(this.state.timer);
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

        // preformat time remaining
        if (key === 'start') {
          const remaining = this.getRemainingTime(value);
          value = this.formatClock(remaining);
        }

        if (key !== 'children') {
          footerItems.push([
            <dd key={item} className={`card-${key}`}>
              <dl>
                <dt>{this.getFooterLabels(item)}</dt>
                <dd ref={key}>{value}</dd>
              </dl>
            </dd>,
          ]);
        }
      }
    }
    return footerItems;
  }

  startGameTimer(timestamp) {
    log.info(this.refs.hours.content);
    const timer = setInterval(() => {
      log.info('1 second');
      const remaining = this.getRemainingTime(timestamp);
      this.refs.hours.textContent = remaining.hours;
      this.refs.minutes.textContent = remaining.minutes;
      this.refs.seconds.textContent = remaining.seconds;
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
    log.info(this.refs);
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
