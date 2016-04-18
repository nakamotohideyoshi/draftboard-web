exports.USER_NOT_AUTHENTICATED = 'USER_NOT_AUTHENTICATED';

// reducers.draft-group-players
exports.FETCHING_DRAFT_GROUPS = 'FETCHING_DRAFT_GROUPS';
exports.FETCH_DRAFTGROUP_SUCCESS = 'FETCH_DRAFTGROUP_SUCCESS';
exports.SET_FOCUSED_PLAYER = 'SET_FOCUSED_PLAYER';
// TODO: FETCH_DRAFTGROUP_REQUEST isn't connected in any reducers.
exports.FETCH_DRAFTGROUP_REQUEST = 'FETCH_DRAFTGROUP_REQUEST';
// TODO: FETCH_DRAFTGROUP_FAIL isn't connected in any reducers.
exports.FETCH_DRAFTGROUP_FAIL = 'FETCH_DRAFTGROUP_FAIL';

// reducers.injuries
exports.FETCH_INJURIES_SUCCESS = 'FETCH_INJURIES_SUCCESS';

// reducers.fantasy-history
exports.FETCH_FANTASY_HISTORY_SUCCESS = 'FETCH_FANTASY_HISTORY_SUCCESS';

// reducers.featured-contests
exports.FETCHING_FEATURED_CONTESTS = 'FETCHING_FEATURED_CONTESTS';
exports.FETCH_FEATURED_CONTESTS_SUCCESS = 'FETCH_FEATURED_CONTESTS_SUCCESS';
exports.FETCH_FEATURED_CONTESTS_FAIL = 'FETCH_FEATURED_CONTESTS_FAIL';

// reducers.upcoming-contests
exports.FETCH_UPCOMING_CONTESTS = 'FETCH_UPCOMING_CONTESTS';
exports.FETCH_UPCOMING_CONTESTS_SUCCESS = 'FETCH_UPCOMING_CONTESTS_SUCCESS';
exports.FETCH_UPCOMING_CONTESTS_FAIL = 'FETCH_UPCOMING_CONTESTS_FAIL';
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

// reducers.entries
exports.RECEIVE_ENTRIES_UPCOMING_LINEUPS = 'RECEIVE_ENTRIES_UPCOMING_LINEUPS';
exports.ADD_ENTRIES_PLAYERS = 'ADD_ENTRIES_PLAYERS';
exports.CONFIRM_RELATED_ENTRIES_INFO = 'CONFIRM_RELATED_ENTRIES_INFO';
exports.REQUEST_ENTRIES = 'REQUEST_ENTRIES';
exports.RECEIVE_ENTRIES = 'RECEIVE_ENTRIES';

// reducers.live
exports.LIVE_MODE_CHANGED = 'LIVE_MODE_CHANGED';

// reducers.live-contests
exports.CONFIRM_RELATED_LIVE_CONTEST_INFO = 'CONFIRM_RELATED_LIVE_CONTEST_INFO';
exports.REQUEST_LIVE_CONTEST_INFO = 'REQUEST_LIVE_CONTEST_INFO';
exports.RECEIVE_LIVE_CONTEST_INFO = 'RECEIVE_LIVE_CONTEST_INFO';
exports.REQUEST_LIVE_CONTEST_LINEUPS = 'REQUEST_LIVE_CONTEST_LINEUPS';
exports.RECEIVE_LIVE_CONTEST_LINEUPS = 'RECEIVE_LIVE_CONTEST_LINEUPS';
exports.REQUEST_LIVE_CONTEST_LINEUPS_USERNAMES = 'REQUEST_LIVE_CONTEST_LINEUPS_USERNAMES';
exports.RECEIVE_LIVE_CONTEST_LINEUPS_USERNAMES = 'RECEIVE_LIVE_CONTEST_LINEUPS_USERNAMES';
exports.REMOVE_LIVE_CONTESTS = 'REMOVE_LIVE_CONTESTS';

// reducers.current-draft-groups
exports.REQUEST_CURRENT_DRAFT_GROUPS = 'REQUEST_CURRENT_DRAFT_GROUPS';
exports.RECEIVE_CURRENT_DRAFT_GROUPS = 'RECEIVE_CURRENT_DRAFT_GROUPS';

// reducers.live-draft-groups
exports.CONFIRM_LIVE_DRAFT_GROUP_STORED = 'CONFIRM_LIVE_DRAFT_GROUP_STORED';
exports.REQUEST_DRAFT_GROUP_BOXSCORES = 'REQUEST_DRAFT_GROUP_BOXSCORES';
exports.RECEIVE_DRAFT_GROUP_BOXSCORES = 'RECEIVE_DRAFT_GROUP_BOXSCORES';
exports.REQUEST_LIVE_DRAFT_GROUP_INFO = 'REQUEST_LIVE_DRAFT_GROUP_INFO';
exports.RECEIVE_LIVE_DRAFT_GROUP_INFO = 'RECEIVE_LIVE_DRAFT_GROUP_INFO';
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
  // email/pass
exports.UPDATE_USER_EMAIL_PASS = 'UPDATE_USER_EMAIL_PASS';
exports.UPDATE_USER_EMAIL_PASS_FAIL = 'UPDATE_USER_EMAIL_PASS_FAIL';
exports.UPDATE_USER_EMAIL_PASS_SUCCESS = 'UPDATE_USER_EMAIL_PASS_SUCCESS';
  // Adddress, dob, etc.
exports.UPDATE_USER_INFO = 'UPDATE_USER_INFO';
exports.UPDATE_USER_INFO_FAIL = 'UPDATE_USER_INFO_FAIL';
exports.UPDATE_USER_INFO_SUCCESS = 'UPDATE_USER_INFO_SUCCESS';
exports.FETCH_USER_INFO = 'FETCH_USER';
exports.FETCH_USER_INFO_FAIL = 'FETCH_USER_FAIL';
exports.FETCH_USER_INFO_SUCCESS = 'FETCH_USER_SUCCESS';
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


// reducers.payments
exports.FETCH_PAYMENTS = 'FETCH_PAYMENTS';
exports.FETCH_PAYMENTS_SUCCESS = 'FETCH_PAYMENTS_SUCCESS';
exports.FETCH_PAYMENTS_FAIL = 'FETCH_PAYMENTS_FAIL';
exports.ADD_PAYMENT_METHOD = 'ADD_PAYMENT_METHOD';
exports.ADD_PAYMENT_METHOD_SUCCESS = 'ADD_PAYMENT_METHOD_SUCCESS';
exports.ADD_PAYMENT_METHOD_FAIL = 'ADD_PAYMENT_METHOD_FAIL';
exports.SET_PAYMENT_METHOD_DEFAULT = 'SET_PAYMENT_METHOD_DEFAULT';
exports.SET_PAYMENT_METHOD_DEFAULT_SUCCESS = 'SET_PAYMENT_METHOD_SUCCESS';
exports.SET_PAYMENT_METHOD_DEFAULT_FAIL = 'SET_PAYMENT_METHOD_DEFAULT_FAIL';
exports.REMOVE_PAYMENT_METHOD = 'REMOVE_PAYMENT_METHOD';
exports.REMOVE_PAYMENT_METHOD_SUCCESS = 'REMOVE_PAYMENT_METHOD_SUCCESS';
exports.REMOVE_PAYMENT_METHOD_FAIL = 'REMOVE_PAYMENT_METHOD_FAIL';
exports.WITHDRAW_AMOUNT = 'WITHDRAW';
exports.WITHDRAW_AMOUNT_FAIL = 'WITHDRAW_FAIL';
exports.WITHDRAW_AMOUNT_SUCCESS = 'WITHDRAW_SUCCESS';
exports.DEPOSIT_AMOUNT = 'DEPOSIT';
exports.DEPOSIT_AMOUNT_FAIL = 'DEPOSIT_FAIL';
exports.DEPOSIT_AMOUNT_SUCCESS = 'DEPOSIT_SUCCESS';

// reducers.results
exports.REQUEST_RESULTS = 'REQUEST_RESULTS';
exports.RECEIVE_RESULTS = 'RECEIVE_RESULTS';

// reducers.lineup-usernames
exports.REQUEST_LINEUP_USERNAMES = 'REQUEST_LINEUP_USERNAMES';
exports.RECEIVE_LINEUP_USERNAMES = 'RECEIVE_LINEUP_USERNAMES';

// player-news-actions
exports.FETCHING_PLAYER_NEWS = 'FETCHING_PLAYER_NEWS';
exports.FETCH_PLAYER_NEWS_SUCCESS = 'FETCH_PLAYER_NEWS_SUCCESS';
exports.FETCH_PLAYER_NEWS_FAIL = 'FETCH_PLAYER_NEWS_FAIL';

// player-history-actions
exports.FETCHING_PLAYER_BOX_SCORE_HISTORY = 'FETCHING_PLAYER_BOX_SCORE_HISTORY';
exports.FETCH_PLAYER_BOX_SCORE_HISTORY_SUCCESS = 'FETCH_PLAYER_BOX_SCORE_HISTORY_SUCCESS';
exports.FETCH_PLAYER_BOX_SCORE_HISTORY_FAIL = 'FETCH_PLAYER_BOX_SCORE_HISTORY_FAIL';
exports.REMOVE_PLAYER_BOX_SCORE_HISTORY = 'REMOVE_PLAYER_BOX_SCORE_HISTORY';

// entry-request-actions
exports.ADD_ENTRY_REQUEST_MONITOR = 'ADD_ENTRY_REQUEST_MONITOR';
exports.ADD_ENTRY_REQUEST_MONITOR_EXISTS = 'ADD_ENTRY_REQUEST_MONITOR_EXISTS';
exports.ENTRY_REQUEST_RECIEVED = 'ENTRY_REQUEST_RECIEVED';
exports.DELETE_ENTRY_REQUEST = 'DELETE_ENTRY_REQUEST';
exports.IGNORING_FETCH_ENTRY_REQUEST = 'IGNORING_FETCH_ENTRY_REQUEST';
exports.FETCHING_ENTRY_REQUEST_STATUS = 'FETCHING_ENTRY_REQUEST_STATUS';

// lineup-edit-request
exports.ADD_LINEUP_EDIT_REQUEST_MONITOR = 'ADD_LINEUP_EDIT_REQUEST_MONITOR';
exports.ADD_LINEUP_EDIT_REQUEST_MONITOR_EXISTS = 'ADD_LINEUP_EDIT_REQUEST_MONITOR_EXISTS';
exports.LINEUP_EDIT_REQUEST_RECIEVED = 'LINEUP_EDIT_REQUEST_RECIEVED';
exports.DELETE_LINEUP_EDIT_REQUEST = 'DELETE_LINEUP_EDIT_REQUEST';
exports.IGNORING_FETCH_LINEUP_EDIT_REQUEST = 'IGNORING_FETCH_LINEUP_EDIT_REQUEST';
exports.FETCHING_LINEUP_EDIT_REQUEST_STATUS = 'FETCHING_LINEUP_EDIT_REQUEST_STATUS';

// message-actions
exports.ADD_MESSAGE = 'ADD_MESSAGE';
exports.REMOVE_MESSAGE = 'REMOVE_MESSAGE';
exports.CLEAR_MESSAGES = 'CLEAR_MESSAGES';

// pusher-live
exports.PUSHER_ADD_ANIMATION_EVENT = 'PUSHER_ADD_ANIMATION_EVENT';
exports.PUSHER_ADD_GAME_QUEUE_EVENT = 'PUSHER_ADD_GAME_QUEUE_EVENT';
exports.PUSHER_ADD_PLAYER_EVENT_DESCRIPTION = 'PUSHER_ADD_PLAYER_EVENT_DESCRIPTION';
exports.PUSHER_DIFFERENCE_PLAYERS_PLAYING = 'PUSHER_DIFFERENCE_PLAYERS_PLAYING';
exports.PUSHER_REMOVE_ANIMATION_EVENT = 'PUSHER_REMOVE_ANIMATION_EVENT';
exports.PUSHER_REMOVE_PLAYER_EVENT_DESCRIPTION = 'PUSHER_REMOVE_PLAYER_EVENT_DESCRIPTION';
exports.PUSHER_SHIFT_GAME_QUEUE_EVENT = 'PUSHER_SHIFT_GAME_QUEUE_EVENT';
exports.PUSHER_UNION_PLAYERS_PLAYING = 'PUSHER_UNION_PLAYERS_PLAYING';
exports.PUSHER_UNSHIFT_PLAYER_HISTORY = 'PUSHER_UNSHIFT_PLAYER_HISTORY';
