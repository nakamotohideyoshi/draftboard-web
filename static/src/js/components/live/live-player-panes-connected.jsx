import React from 'react'
import * as ReactRedux from 'react-redux'
import renderComponent from '../../lib/render-component'
import store from '../../store'


import LivePlayerPane from './live-player-pane'


const LivePlayerPanes = React.createClass({
  propTypes: {
    playerLeft: React.PropTypes.object,
    playerRight: React.PropTypes.object
  },

  render: function() {
    return (
      <div>
        <LivePlayerPane side='left' player={this.props.playerLeft} />
        <LivePlayerPane side='right' player={this.props.playerRight} />
      </div>
    )
  }
})



let {Provider, connect} = ReactRedux


function mapStateToProps(state) {
  return {
    'playerLeft': {
      'position': 'Cleveland Cavailers - SF #23',
      'name': 'Lebron Left James',
      'pts': 27.5,
      'owned': '18%',
      'img': '',
      'stats': [
        {
          'name': 'avg',
          'score': 42.5
        },
        {
          'name': 'avg',
          'score': 42.5
        },
        {
          'name': 'avg',
          'score': 42.5
        },
        {
          'name': 'avg',
          'score': 42.5
        },
        {
          'name': 'avg',
          'score': 42.5
        },
        {
          'name': 'avg',
          'score': 42.5
        }
      ],
      'game': {
        'time': '3:48',
        'part': '4th',
        'teamA': {
          'points': 103,
          'logo': '...'
        },
        'teamB': {
          'points': 92,
          'logo': '...'
        }
      },
      'activities': [
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        }
      ]
    },
    'playerRight': {
      'position': 'Cleveland Cavailers - SF #23',
      'name': 'Lebron Right James',
      'pts': 27.5,
      'owned': '18%',
      'img': '',
      'stats': [
        {
          'name': 'avg',
          'score': 42.5
        },
        {
          'name': 'avg',
          'score': 42.5
        },
        {
          'name': 'avg',
          'score': 42.5
        },
        {
          'name': 'avg',
          'score': 42.5
        },
        {
          'name': 'avg',
          'score': 42.5
        },
        {
          'name': 'avg',
          'score': 42.5
        }
      ],
      'game': {
        'time': '3:48',
        'part': '4th',
        'teamA': {
          'points': 103,
          'logo': '...'
        },
        'teamB': {
          'points': 92,
          'logo': '...'
        }
      },
      'activities': [
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        },
        {
          'description': "Lebron James assists Russel Westbrook's 3-pointer",
          'points': '+2',
          'time': '4:13 - 4th'
        }
      ]
    }
  }
}


var LivePlayerPanesConnected = connect(
  mapStateToProps
)(LivePlayerPanes)


export default LivePlayerPanesConnected
