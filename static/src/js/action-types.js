// Since we don't always need to fire off actions via the API middleware, this
// can be used to prevent redux from complaining about misspelled actions.
exports.NULL = 'NULL';
exports.USER_NOT_AUTHENTICATED = 'USER_NOT_AUTHENTICATED';

// reducers.draft-group-players
exports.FETCHING_DRAFT_GROUPS = 'FETCHING_DRAFT_GROUPS';
exports.FETCH_DRAFTGROUP_SUCCESS = 'FETCH_DRAFTGROUP_SUCCESS';
exports.SET_FOCUSED_PLAYER = 'SET_FOCUSED_PLAYER';
// TODO: FETCH_DRAFTGROUP_REQUEST isn't connected in any reducers.
exports.FETCH_DRAFTGROUP_REQUEST = 'FETCH_DRAFTGROUP_REQUEST';
// TODO: FETCH_DRAFTGROUP_FAIL isn't connected in any reducers.
exports.FETCH_DRAFTGROUP_FAIL = 'FETCH_DRAFTGROUP_FAIL';

// reducers.upcoming-draft-group-game-updates
exports.DRAFT_GROUP_UPDATES__FETCHING = 'DRAFT_GROUP_UPDATES__FETCHING';
exports.DRAFT_GROUP_UPDATES__FETCHING_NULL = 'DRAFT_GROUP_UPDATES__FETCHING_NULL';
exports.DRAFT_GROUP_UPDATES__FETCH_SUCCESS = 'DRAFT_GROUP_UPDATES__FETCH_SUCCESS';
exports.DRAFT_GROUP_UPDATES__FETCH_FAIL = 'DRAFT_GROUP_UPDATES__FETCH_FAIL';

// reducers.fantasy-history
exports.FANTASY_HISTORY__FETCHING = 'FANTASY_HISTORY__FETCHING';
exports.FANTASY_HISTORY__FETCH_SUCCESS = 'FANTASY_HISTORY__FETCH_SUCCESS';
exports.FANTASY_HISTORY__FETCH_FAIL = 'FANTASY_HISTORY__FETCH_FAIL';

// reducers.featured-contests
exports.FETCHING_FEATURED_CONTESTS = 'FETCHING_FEATURED_CONTESTS';
exports.FETCH_FEATURED_CONTESTS_SUCCESS = 'FETCH_FEATURED_CONTESTS_SUCCESS';
exports.FETCH_FEATURED_CONTESTS_FAIL = 'FETCH_FEATURED_CONTESTS_FAIL';

// reducers.contest-pools
exports.FETCH_CONTEST_POOLS = 'FETCH_CONTEST_POOLS';
exports.FETCH_CONTEST_POOLS_SUCCESS = 'FETCH_CONTEST_POOLS_SUCCESS';
exports.FETCH_CONTEST_POOLS_FAIL = 'FETCH_CONTEST_POOLS_FAIL';
exports.UPCOMING_CONTESTS_FILTER_CHANGED = 'UPCOMING_CONTESTS_FILTER_CHANGED';
exports.SET_FOCUSED_CONTEST = 'SET_FOCUSED_CONTEST';
exports.UPCOMING_CONTESTS_ORDER_CHANGED = 'UPCOMING_CONTESTS_ORDER_CHANGED';
exports.FETCHING_CONTEST_ENTRANTS = 'FETCHING_CONTEST_ENTRANTS';
exports.FETCH_CONTEST_ENTRANTS_SUCCESS = 'FETCH_CONTEST_ENTRANTS_SUCCESS';
exports.FETCH_CONTEST_ENTRANTS_FAIL = 'FETCH_CONTEST_ENTRANTS_FAIL';
exports.UPCOMING_CONTESTS_UPDATE_RECEIVED = 'UPCOMING_CONTESTS_UPDATE_RECEIVED';

// reducers.contest-pool-entries
exports.FETCHING_CONTEST_POOL_ENTRIES = 'FETCHING_CONTEST_POOL_ENTRIES';
exports.FETCH_CONTEST_POOL_ENTRIES_SUCCESS = 'FETCH_CONTEST_POOL_ENTRIES_SUCCESS';
exports.FETCH_CONTEST_POOL_ENTRIES_FAIL = 'FETCH_CONTEST_POOL_ENTRIES_FAIL';

exports.REMOVING_CONTEST_POOL_ENTRY = 'REMOVING_CONTEST_POOL_ENTRY';
exports.REMOVING_CONTEST_POOL_ENTRY_SUCCESS = 'REMOVE_CONTEST_POOL_ENTRY_SUCCESS';
exports.REMOVING_CONTEST_POOL_ENTRY_FAIL = 'REMOVE_CONTEST_POOL_ENTRY_FAIL';

exports.ENTERING_CONTEST_POOL = 'ENTERING_CONTEST_POOL';
exports.ENTERING_CONTEST_POOL_SUCCESS = 'ENTERING_CONTEST_POOL_SUCCESS';
exports.ENTERING_CONTEST_POOL_FAIL = 'ENTERING_CONTEST_POOL_FAIL';


// reducers.upcoming-draft-groups-info
exports.FETCH_UPCOMING_DRAFTGROUPS_INFO = 'FETCH_UPCOMING_DRAFTGROUPS_INFO';
exports.FETCH_UPCOMING_DRAFTGROUPS_INFO_SUCCESS = 'FETCH_UPCOMING_DRAFTGROUPS_INFO_SUCCESS';
exports.FETCH_UPCOMING_DRAFTGROUPS_INFO_FAIL = 'FETCH_UPCOMING_DRAFTGROUPS_INFO_FAIL';
exports.CLOSE_DRAFT_GROUP_SELECTION_MODAL = 'CLOSE_DRAFT_GROUP_SELECTION_MODAL';
exports.OPEN_DRAFT_GROUP_SELECTION_MODAL = 'OPEN_DRAFT_GROUP_SELECTION_MODAL';
exports.SET_ACTIVE_DRAFT_GROUP_ID = 'SET_ACTIVE_DRAFT_GROUP_ID';
exports.DRAFTGROUP_FILTER_CHANGED = 'DRAFTGROUP_FILTER_CHANGED';
exports.DRAFTGROUP_ORDER_CHANGED = 'DRAFTGROUP_ORDER_CHANGED';
exports.FETCHING_DRAFTGROUP_BOX_SCORES = 'FETCHING_DRAFTGROUP_BOX_SCORES';
exports.FETCH_DRAFTGROUP_BOX_SCORES_FAIL = 'FETCH_DRAFTGROUP_BOX_SCORES_FAIL';
exports.FETCH_DRAFTGROUP_BOX_SCORES_SUCCESS = 'FETCH_DRAFTGROUP_BOX_SCORES_SUCCESS';

// reducers.current-lineups
exports.CURRENT_LINEUPS__ADD_PLAYERS = 'CURRENT_LINEUPS__ADD_PLAYERS';
exports.CURRENT_LINEUPS__RECEIVE = 'CURRENT_LINEUPS__RECEIVE';
exports.CURRENT_LINEUPS__RELATED_INFO_SUCCESS = 'CURRENT_LINEUPS__RELATED_INFO_SUCCESS';
exports.CURRENT_LINEUPS__REQUEST = 'CURRENT_LINEUPS__REQUEST';
exports.CURRENT_LINEUPS_ROSTERS__RECEIVE = 'CURRENT_LINEUPS_ROSTERS__RECEIVE';
exports.CURRENT_LINEUPS_ROSTERS__REQUEST = 'CURRENT_LINEUPS_ROSTERS__REQUEST';

// reducers.lineups
exports.LINEUP_FOCUSED = 'LINEUP_FOCUSED';
exports.LINEUP_HOVERED = 'LINEUP_HOVERED';
exports.FETCH_UPCOMING_LINEUPS = 'FETCH_UPCOMING_LINEUPS';
exports.FETCH_UPCOMING_LINEUPS_FAIL = 'FETCH_UPCOMING_LINEUPS_FAIL';
exports.FETCH_UPCOMING_LINEUPS_SUCCESS = 'FETCH_UPCOMING_LINEUPS_SUCCESS';
exports.EDIT_LINEUP_INIT = 'EDIT_LINEUP_INIT';
exports.FILTER_UPCOMING_LINEUPS_BY_DRAFTGROUP_ID = 'FILTER_UPCOMING_LINEUPS_BY_DRAFTGROUP_ID';

// reducers.create-lineup
exports.SAVE_LINEUP_EDIT = 'SAVE_LINEUP_EDIT';
exports.SAVE_LINEUP_EDIT_FAIL = 'SAVE_LINEUP_EDIT_FAIL';
exports.SAVE_LINEUP_EDIT_SUCCESS = 'SAVE_LINEUP_EDIT_SUCCESS';
exports.CREATE_LINEUP_INIT = 'CREATE_LINEUP_INIT';
exports.CREATE_LINEUP_ADD_PLAYER = 'CREATE_LINEUP_ADD_PLAYER';
exports.CREATE_LINEUP_REMOVE_PLAYER = 'CREATE_LINEUP_REMOVE_PLAYER';
exports.CREATE_LINEUP_SAVE = 'CREATE_LINEUP_SAVE';
exports.CREATE_LINEUP_SAVE_FAIL = 'CREATE_LINEUP_SAVE_FAIL';
exports.CREATE_LINEUP_SET_TITLE = 'CREATE_LINEUP_SET_TITLE';
exports.CREATE_LINEUP_IMPORT = 'CREATE_LINEUP_IMPORT';

exports.ADD_CONTEST = 'ADD_CONTEST';
exports.REMOVE_CONTEST = 'REMOVE_CONTEST';
exports.UPDATE_CONTEST = 'UPDATE_CONTEST';

// reducers.current-lineups
exports.SET_CURRENT_LINEUPS = 'SET_CURRENT_LINEUPS';

// reducers.live-players
exports.REQUEST_LIVE_PLAYERS_STATS = 'REQUEST_LIVE_PLAYERS_STATS';
exports.RECEIVE_LIVE_PLAYERS_STATS = 'RECEIVE_LIVE_PLAYERS_STATS';
exports.UPDATE_LIVE_PLAYER_STATS = 'UPDATE_LIVE_PLAYER_STATS';

// reducers.live-contests
exports.CONFIRM_RELATED_LIVE_CONTEST_INFO = 'CONFIRM_RELATED_LIVE_CONTEST_INFO';
exports.REQUEST_CONTEST_POOL_INFO = 'REQUEST_CONTEST_POOL_INFO';
exports.RECEIVE_CONTEST_POOL_INFO = 'RECEIVE_CONTEST_POOL_INFO';
exports.REQUEST_LIVE_CONTEST_LINEUPS = 'REQUEST_LIVE_CONTEST_LINEUPS';
exports.RECEIVE_LIVE_CONTEST_LINEUPS = 'RECEIVE_LIVE_CONTEST_LINEUPS';
exports.REQUEST_LIVE_CONTEST_LINEUPS_USERNAMES = 'REQUEST_LIVE_CONTEST_LINEUPS_USERNAMES';
exports.RECEIVE_LIVE_CONTEST_LINEUPS_USERNAMES = 'RECEIVE_LIVE_CONTEST_LINEUPS_USERNAMES';
exports.REMOVE_LIVE_CONTESTS = 'REMOVE_LIVE_CONTESTS';

// reducers.live-draft-groups
exports.CONFIRM_LIVE_DRAFT_GROUP_STORED = 'CONFIRM_LIVE_DRAFT_GROUP_STORED';
exports.REQUEST_DRAFT_GROUP_BOXSCORES = 'REQUEST_DRAFT_GROUP_BOXSCORES';
exports.RECEIVE_DRAFT_GROUP_BOXSCORES = 'RECEIVE_DRAFT_GROUP_BOXSCORES';
exports.LIVE_DRAFT_GROUP__INFO__REQUEST = 'LIVE_DRAFT_GROUP__INFO__REQUEST';
exports.LIVE_DRAFT_GROUP__INFO__RECEIVE = 'LIVE_DRAFT_GROUP__INFO__RECEIVE';
exports.REQUEST_LIVE_DRAFT_GROUP_FP = 'REQUEST_LIVE_DRAFT_GROUP_FP';
exports.RECEIVE_LIVE_DRAFT_GROUP_FP = 'RECEIVE_LIVE_DRAFT_GROUP_FP';
exports.UPDATE_LIVE_DRAFT_GROUP_PLAYER_FP = 'UPDATE_LIVE_DRAFT_GROUP_PLAYER_FP';
exports.REMOVE_LIVE_DRAFT_GROUPS = 'REMOVE_LIVE_DRAFT_GROUPS';

// reducers.prizes
exports.REQUEST_PRIZE = 'REQUEST_PRIZE';
exports.RECEIVE_PRIZE = 'RECEIVE_PRIZE';

// reducers.sports
exports.REQUEST_TEAMS = 'REQUEST_TEAMS';
exports.RECEIVE_TEAMS = 'RECEIVE_TEAMS';
exports.REQUEST_GAMES = 'REQUEST_GAMES';
exports.RECEIVE_GAMES = 'RECEIVE_GAMES';
exports.UPDATE_GAME = 'UPDATE_GAME';

// reducers.transactions
exports.FETCH_TRANSACTIONS = 'FETCH_TRANSACTIONS';
exports.FETCH_TRANSACTIONS_SUCCESS = 'FETCH_TRANSACTIONS_SUCCESS';
exports.FETCH_TRANSACTIONS_FAIL = 'FETCH_TRANSACTIONS_FAIL';
exports.FILTER_TRANSACTIONS = 'FILTER_TRANSACTIONS';
exports.TRANSACTION_FOCUSED = 'TRANSACTION_FOCUSED';

// reducers.user
  // basic user info
exports.FETCH_USER = 'FETCH_USER';
exports.FETCH_USER__FAIL = 'FETCH_USER__FAIL';
exports.FETCH_USER__SUCCESS = 'FETCH_USER__SUCCESS';
  // email/pass
exports.UPDATE_USER_EMAIL_PASS = 'UPDATE_USER_EMAIL_PASS';
exports.UPDATE_USER_EMAIL_PASS_FAIL = 'UPDATE_USER_EMAIL_PASS_FAIL';
exports.UPDATE_USER_EMAIL_PASS_SUCCESS = 'UPDATE_USER_EMAIL_PASS_SUCCESS';
  // Adddress, dob, etc.
exports.UPDATE_USER_INFO = 'UPDATE_USER_INFO';
exports.UPDATE_USER_INFO_FAIL = 'UPDATE_USER_INFO_FAIL';
exports.UPDATE_USER_INFO_SUCCESS = 'UPDATE_USER_INFO_SUCCESS';
exports.FETCH_USER_INFO = 'FETCH_USER_INFO';
exports.FETCH_USER_INFO_FAIL = 'FETCH_USER_INFO__FAIL';
exports.FETCH_USER_INFO_SUCCESS = 'FETCH_USER_INFO__SUCCESS';
  // Email notification settings
exports.UPDATE_EMAIL_NOTIFICATIONS = 'UPDATE_EMAIL_NOTIFICATIONS';
exports.UPDATE_EMAIL_NOTIFICATIONS_FAIL = 'UPDATE_EMAIL_NOTIFICATIONS_FAIL';
exports.UPDATE_EMAIL_NOTIFICATIONS_SUCCESS = 'UPDATE_EMAIL_NOTIFICATIONS_SUCCESS';
exports.FETCH_EMAIL_NOTIFICATIONS = 'FETCH_EMAIL_NOTIFICATIONS';
exports.FETCH_EMAIL_NOTIFICATIONS_FAIL = 'FETCH_EMAIL_NOTIFICATIONS_FAIL';
exports.FETCH_EMAIL_NOTIFICATIONS_SUCCESS = 'FETCH_EMAIL_NOTIFICATIONS_SUCCESS';
  // Cash balance
exports.FETCHING_CASH_BALANCE = 'FETCHING_CASH_BALANCE';
exports.FETCH_CASH_BALANCE_FAIL = 'FETCH_CASH_BALANCE_FAIL';
exports.FETCH_CASH_BALANCE_SUCCESS = 'FETCH_CASH_BALANCE_SUCCESS';
  // IP location verification
exports.VERIFY_LOCATION = 'VERIFY_LOCATION';
  // Trulioo identity verification
exports.VERIFY_IDENTITY__SEND = 'VERIFY_IDENTITY__SEND';
exports.VERIFY_IDENTITY__FAIL = 'VERIFY_IDENTITY__FAIL';
exports.VERIFY_IDENTITY__SUCCESS = 'VERIFY_IDENTITY__SUCCESS';

// reducers.payments
exports.WITHDRAW_FUNDS = 'WITHDRAW_FUNDS';
exports.WITHDRAW_FUNDS_FAIL = 'WITHDRAW_FUNDS_FAIL';
exports.WITHDRAW_FUNDS_SUCCESS = 'WITHDRAW_FUNDS_SUCCESS';
exports.DEPOSITING = 'DEPOSITING';
exports.DEPOSIT_FAIL = 'DEPOSIT_FAIL';
exports.DEPOSIT_SUCCESS = 'DEPOSIT_SUCCESS';
// PayPal
exports.FETCHING_PAYPAL_CLIENT_TOKEN = 'FETCHING_PAYPAL_CLIENT_TOKEN';
exports.FETCH_PAYPAL_CLIENT_TOKEN_SUCCESS = 'FETCH_PAYPAL_CLIENT_TOKEN_SUCCESS';
exports.FETCH_PAYPAL_CLIENT_TOKEN_FAIL = 'FETCH_PAYPAL_CLIENT_TOKEN_FAIL';
exports.PAYPAL_NONCE_RECEIVED = 'PAYPAL_NONCE_RECEIVED';
exports.PAYPAL_CANCELLED = 'PAYPAL_CANCELLED';
exports.PAYPAL_CANCELLED = 'PAYPAL_AMOUNT_CHANGED';


// reducers.results
exports.REQUEST_RESULTS = 'REQUEST_RESULTS';
exports.RECEIVE_RESULTS = 'RECEIVE_RESULTS';

// reducers.lineup-usernames
exports.REQUEST_LINEUP_USERNAMES = 'REQUEST_LINEUP_USERNAMES';
exports.RECEIVE_LINEUP_USERNAMES = 'RECEIVE_LINEUP_USERNAMES';


// player-history-actions
exports.PLAYER_HISTORY_SINGLE__REQUEST = 'PLAYER_HISTORY_SINGLE__REQUEST';
exports.PLAYER_HISTORY_SINGLE__RECEIVE = 'PLAYER_HISTORY_SINGLE__RECEIVE';


// lineup-edit-request
exports.LINEUP_EDIT_REQUEST_RECIEVED = 'LINEUP_EDIT_REQUEST_RECIEVED';
exports.DELETE_LINEUP_EDIT_REQUEST = 'DELETE_LINEUP_EDIT_REQUEST';
exports.IGNORING_FETCH_LINEUP_EDIT_REQUEST = 'IGNORING_FETCH_LINEUP_EDIT_REQUEST';
exports.FETCHING_LINEUP_EDIT_REQUEST_STATUS = 'FETCHING_LINEUP_EDIT_REQUEST_STATUS';

// message-actions
exports.ADD_MESSAGE = 'ADD_MESSAGE';
exports.REMOVE_MESSAGE = 'REMOVE_MESSAGE';
exports.CLEAR_MESSAGES = 'CLEAR_MESSAGES';

// live-multipart-events
exports.EVENT_MULTIPART_SET = 'EVENT_MULTIPART_SET';
exports.EVENT_MULTIPART_DELETE = 'EVENT_MULTIPART_DELETE';
exports.EVENT_MULTIPART_MERGE_PLAYERS = 'EVENT_MULTIPART_MERGE_PLAYERS';
exports.EVENT_MULTIPART_OMIT_PLAYERS = 'EVENT_MULTIPART_OMIT_PLAYERS';

// events
exports.EVENT__SHOW_CURRENT_RESULT = 'EVENT__SHOW_CURRENT_RESULT';
exports.EVENT__SET_CURRENT = 'EVENT__SET_CURRENT';
exports.EVENT_GAME_QUEUE_PUSH = 'EVENT_GAME_QUEUE_PUSH';
exports.EVENT_PLAYER_ADD_DESCRIPTION = 'EVENT_PLAYER_ADD_DESCRIPTION';
exports.EVENT_REMOVE_PLAYERS_PLAYING = 'EVENT_REMOVE_PLAYERS_PLAYING';
exports.EVENT__REMOVE_CURRENT = 'EVENT__REMOVE_CURRENT';
exports.EVENT_PLAYER_REMOVE_DESCRIPTION = 'EVENT_PLAYER_REMOVE_DESCRIPTION';
exports.EVENT_SHIFT_GAME_QUEUE = 'EVENT_SHIFT_GAME_QUEUE';
exports.EVENT_UNION_PLAYERS_PLAYING = 'EVENT_UNION_PLAYERS_PLAYING';
exports.EVENT_UNSHIFT_PLAYER_HISTORY = 'EVENT_UNSHIFT_PLAYER_HISTORY';

// reducers.watching
exports.WATCHING_UPDATE = 'WATCHING_UPDATE';
exports.WATCHING__RESET = 'WATCHING__RESET';

// reducers.async_failures
exports.ADD_ASYNC_FAILURE = 'ADD_ASYNC_FAILURE';
exports.REMOVE_ASYNC_FAILURE = 'REMOVE_ASYNC_FAILURE';
