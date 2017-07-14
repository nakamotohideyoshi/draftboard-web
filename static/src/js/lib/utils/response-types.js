/**
 * Because the API is rather inconsistent with error messaging, this is a handful of helpful
 * functions to determine what kind of data was returned from an request.
 *
 * NOTE: These should only be used on 4xx/5xx responses, it is assumed that we've already determined
 * the response is an error.
 */


/**
 * If a serializer is used on the server, it responds to validataion errors with an object full of
 * field errors.
 *
 * {
 *  "email": ['field cannot be blank'],
 *  "username": ['field cannot be blank', 'name taken'],
 * }
 */
export function isFieldValidationErrorObject(res) {
  /**
   * Check if the body is:
   *    - an object
   *    - NOT an array (because if you typeof() an Array you get 'object')
   *    - that the object has keys
   */
  if (res.body && typeof(res.body) === 'object' && !Array.isArray(res.body) &&
    Object.keys(res.body).length > 0
  ) {
    // Since generic Exception details (as shown in isExceptionDetail) don't contain any specific
    // field errors, this is NOT truthy for anything that only has a 'detail' key.
    if (Object.keys(res.body).length === 1 && 'detail' in res.body) {
      return false;
    }

    return true;
  }

  return false;
}


/**
 *  When an APIException is thrown without providing any field info, we get a response similar to
 *  the field validation error response but with only a 'detail' field. and it's a string.
 *
 * {
 *  "detail": "something is wrong."
 * }
 */
export function isExceptionDetail(res) {
  return (
    res &&
    res.body &&
    typeof(res.body) === 'object' &&
    !Array.isArray(res.body) &&
    'detail' in res.body &&
    !Array.isArray(res.body.detail) &&
    Object.keys(res.body).length === 1
  );
}


/**
 * Sometimes we get an array of errors (I've only ever seen these contain a single element).
 *
 * ['something is wrong.']
 */
export function isListOfErrors(res) {
  return Array.isArray(res.body) && res.body.length > 0;
}


/**
 * If an exception is thrown without doing the proper things, we just get a string of text back.
 *
 * 'something is wrong'
 */
export function isRawTextError(res) {
  return typeof(res.body) === 'string';
}


/**
 * Unpack the body of a fetch response and format it as json. This is necessary because our API
 * responses are in varied formats.
 *
 * @param  {Object} res A fetch response
 * @return {Object}     An object literal, or the json response.
 */
export function getJsonResponse(res) {
  // If it's jSON, unpack and return it.
  if (res.headers.get('Content-Type') === 'application/json') {
    return res.json();
  }

  // If it's text, unpack it and add the text as the 'detail' key of an object literal so it
  // can be used as if it were a json response.
  return res.text().then((text) => ({ detail: text }));
}


export function getErrorMessage(res) {
  if (isFieldValidationErrorObject(res)) {
    return res.body.detail;
  }

  if (isExceptionDetail(res)) {
    return res.body.detail;
  }

  if (isListOfErrors(res)) {
    return res.body;
  }

  if (isRawTextError(res)) {
    return res.body;
  }

  return '';
}
