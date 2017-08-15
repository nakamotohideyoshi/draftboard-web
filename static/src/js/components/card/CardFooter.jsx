import React from 'react';
import moment from 'moment';
import PropTypes from 'prop-types';

class CardFooter extends React.Component {
  componentDidMount() {
    if (this.props.start) {
      this.startGameTimer(this.props.start);
    }
  }

  // timer cleanup
  componentWillUnmount() {
    clearInterval(this.state.timer);
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
      dateobj.hours = durationhours;
      dateobj.minutes = durationminutes;
      dateobj.seconds = durartionseconds;
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
          value = `${remaining.hours}:${remaining.minutes}:${remaining.seconds}`;
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
    const timer = setInterval(() => {
      const remaining = this.getRemainingTime(timestamp);
      this.refs.start.textContent = `${remaining.hours}:${remaining.minutes}:${remaining.seconds}`;
    }, 1000);

    this.setState({ timer });
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
  fees: PropTypes.integer,
  entries: PropTypes.integer,
  start: PropTypes.string,
  playeravg: PropTypes.string,
  remsalary: PropTypes.string,
};

export default CardFooter;
