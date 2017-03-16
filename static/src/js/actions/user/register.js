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
 */
export const registerUser = (first, last, birthDay, birthMonth, birthYear, postalCode, email,
      username, password) =>
  fetch(`${API_DOMAIN}/api/account/register/`, {
    credentials: 'same-origin',
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': Cookies.get('csrftoken'),
    },
    body: JSON.stringify({
      first,
      last,
      email,
      username,
      password,
      birth_day: birthDay,
      birth_month: birthMonth,
      birth_year: birthYear,
      postal_code: postalCode,
    }),
  }).then(response => {
    // First, reject a response that isn't in the 200 range.
    if (!response.ok) {
      logAction.error('API post failed:', response);
      return response.json().then(json => Promise.reject(json));
    }

    return { success: true };
  });
