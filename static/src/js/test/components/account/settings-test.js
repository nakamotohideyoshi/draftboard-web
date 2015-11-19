/**
 * TODO:
 *
 * These are tests connected with the main settings of a user
 *
 * SO seperated in sections:
 *
 * - base settings (email, password, email notifications):
 *   - rendering of the component
 *   - on initial it only displays field
 *   - edit button, when clicked `form` in DOM should be present
 *   - mock superagent and POST requests responses with errors in them:
 *     - on error divs with form-field--error should be in the dom (so form stays in DOM)
 *     - on successfull POST, no `form` in the DOM, show back the info with edit button
 *     - if store is updated as it should (there we keep form errors, user data and etc.)
 *
 *
 * - user information settings (addresses + zip code etc.)
 *   - rendering of the component
 *   - on initial it only displays info
 *   - when edit button is clicked `form` in DOM should be present (we show the form)
 *   - addressses for every specific payment type (for future to come prolly)
 *   - reusable component that will be used accross pages
 *
 */
