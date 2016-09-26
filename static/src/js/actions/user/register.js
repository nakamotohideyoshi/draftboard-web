import Cookies from 'js-cookie';
import log from '../../lib/logging';

// get custom logger for actions
const logAction = log.getLogger('action');

// custom API domain for local dev testing
const { API_DOMAIN = '' } = process.env;


/**
 * Fetch wrapper to register a user at /api/account/register/
 * @param  {string} email           Email address
 * @param  {string} username        Wanted username
 * @param  {string} password        Pass
 * @param  {string} passwordConfirm Pass that matches password field
 * @return {mixed}                  True if successful, error json if not
 */
export const registerUser = (email, username, password, passwordConfirm) =>
  fetch(`${API_DOMAIN}/api/account/register/`, {
    credentials: 'same-origin',
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': Cookies.get('csrftoken'),
    },
    body: JSON.stringify({
      email,
      password,
      password_confirm: passwordConfirm,
      username,
    }),
  }).then(response => {
    // First, reject a response that isn't in the 200 range.
    if (!response.ok) {
      logAction.error('API post failed:', response);
      return response.json().then(json => Promise.reject(json));
    }

    return { success: true };
  });
