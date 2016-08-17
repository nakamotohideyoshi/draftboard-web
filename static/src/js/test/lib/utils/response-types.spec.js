import { assert } from 'chai';
import merge from 'lodash/merge';
import * as responseTypes from '../../../lib/utils/response-types';


const fieldValidationError = { body: {
  email: ['field cannot be blank'],
  username: ['field cannot be blank', 'name taken'],
} };
const APIException = { body: { detail: 'something is wrong.' } };
const listOfErrors = { body: ['something is wrong.'] };
const rawTextError = { body: 'something is wrong' };
// take the regular valid one and add a 'detail' field.
const fvWithDetail = merge({}, fieldValidationError);
fvWithDetail.body.detail = 'something is wrong';


describe('utils.responseTypes.isFieldValidationErrorObject', () => {
  it('should be true on a field validation error response', () => {
    assert.isTrue(responseTypes.isFieldValidationErrorObject(fieldValidationError));
  });

  it('should be false on an API exception response', () => {
    assert.isFalse(responseTypes.isFieldValidationErrorObject(APIException));
  });

  it('should be true for a response with a detail field, and also something else', () => {
    assert.isTrue(responseTypes.isFieldValidationErrorObject(fvWithDetail));
  });

  it('should be false on a list of errors response', () => {
    assert.isFalse(responseTypes.isFieldValidationErrorObject(listOfErrors));
  });

  it('should be false on a list of errors response', () => {
    assert.isFalse(responseTypes.isFieldValidationErrorObject(rawTextError));
  });
});


describe('utils.responseTypes.isExceptionDetail', () => {
  it('should be false on a field validation error response', () => {
    assert.isFalse(responseTypes.isExceptionDetail(fieldValidationError));
  });

  it('should be true on an API exception response', () => {
    assert.isTrue(responseTypes.isExceptionDetail(APIException));
  });

  it('should be false for a response with a detail field, and also something else', () => {
    assert.isFalse(responseTypes.isExceptionDetail(fvWithDetail));
  });

  it('should be false on a list of errors response', () => {
    assert.isFalse(responseTypes.isExceptionDetail(listOfErrors));
  });

  it('should be false on a list of errors response', () => {
    assert.isFalse(responseTypes.isExceptionDetail(rawTextError));
  });
});


describe('utils.responseTypes.isListOfErrors', () => {
  it('should be false on a field validation error response', () => {
    assert.isFalse(responseTypes.isListOfErrors(fieldValidationError));
  });

  it('should be false on an API exception response', () => {
    assert.isFalse(responseTypes.isListOfErrors(APIException));
  });

  it('should be false for a response with a detail field, and also something else', () => {
    assert.isFalse(responseTypes.isListOfErrors(fvWithDetail));
  });

  it('should be true on a list of errors response', () => {
    assert.isTrue(responseTypes.isListOfErrors(listOfErrors));
  });

  it('should be false on a list of errors response', () => {
    assert.isFalse(responseTypes.isListOfErrors(rawTextError));
  });
});


describe('utils.responseTypes.isRawTextError', () => {
  it('should be false on a field validation error response', () => {
    assert.isFalse(responseTypes.isRawTextError(fieldValidationError));
  });

  it('should be false on an API exception response', () => {
    assert.isFalse(responseTypes.isRawTextError(APIException));
  });

  it('should be false for a response with a detail field, and also something else', () => {
    assert.isFalse(responseTypes.isRawTextError(fvWithDetail));
  });

  it('should be false on a list of errors response', () => {
    assert.isFalse(responseTypes.isRawTextError(listOfErrors));
  });

  it('should be true on a list of errors response', () => {
    assert.isTrue(responseTypes.isRawTextError(rawTextError));
  });
});
