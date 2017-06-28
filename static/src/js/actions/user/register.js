import Cookies from 'js-cookie';
import log from '../../lib/logging';

// get custom logger for actions
const logAction = log.getLogger('action');

// custom API domain for local dev testing
const { API_DOMAIN = '' } = process.env;


/**
 * Fetch wrapper to register a user at /api/account/register/

 * @param first
 * @param last
 * @param birthDay
 * @param birthMonth
 * @param birthYear
 * @param postalCode
 * @param email
 * @param username
 * @param password
 * @param signupAnyway
 */
export const registerUser = (username, email, password) =>
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
      username,
      password,
    }),
  }).then(response => {
    // First, reject a response that isn't in the 200 range.
    if (!response.ok) {
      logAction.error('API post failed:', response);
      return response.json().then(json => Promise.reject(json));
    }

    return { success: true };
  });
