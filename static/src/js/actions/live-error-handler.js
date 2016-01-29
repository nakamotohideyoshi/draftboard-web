import Raven from 'raven-js'
import { addMessage } from './message-actions.js'


export default (exception, content) => (dispatch) => {
  Raven.captureException(exception)

  dispatch(addMessage({
    level: 'warning',
    content,
  }))
}
