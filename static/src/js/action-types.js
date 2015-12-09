exports.ADD_CONTEST = 'ADD_CONTEST'
exports.REMOVE_CONTEST = 'REMOVE_CONTEST'
exports.UPDATE_CONTEST = 'UPDATE_CONTEST'

exports.USER_NOT_AUTHENTICATED = 'USER_NOT_AUTHENTICATED'

// reducers.draft-groups
exports.FETCHING_DRAFT_GROUPS = 'FETCHING_DRAFT_GROUPS'
exports.FETCH_DRAFTGROUP_REQUEST = 'FETCH_DRAFTGROUP_REQUEST'
exports.FETCH_DRAFTGROUP_SUCCESS = 'FETCH_DRAFTGROUP_SUCCESS'
exports.FETCH_DRAFTGROUP_FAIL = 'FETCH_DRAFTGROUP_FAIL'
exports.SET_FOCUSED_PLAYER = 'SET_FOCUSED_PLAYER'
exports.DRAFTGROUP_FILTER_CHANGED = 'DRAFTGROUP_FILTER_CHANGED'

// reducers.injuries
exports.FETCH_INJURIES_SUCCESS = 'FETCH_INJURIES_SUCCESS'

// reducers.fantasy-history
exports.FETCH_FANTASY_HISTORY_SUCCESS = 'FETCH_FANTASY_HISTORY_SUCCESS'

// reducers.featured-contests
exports.FETCHING_FEATURED_CONTESTS = 'FETCHING_FEATURED_CONTESTS'
exports.FETCH_FEATURED_CONTESTS_SUCCESS = 'FETCH_FEATURED_CONTESTS_SUCCESS'
exports.FETCH_FEATURED_CONTESTS_FAIL = 'FETCH_FEATURED_CONTESTS_FAIL'

// reducers.upcoming-contests
exports.FETCH_UPCOMING_CONTESTS = 'FETCH_UPCOMING_CONTESTS'
exports.FETCH_UPCOMING_CONTESTS_SUCCESS = 'FETCH_UPCOMING_CONTESTS_SUCCESS'
exports.FETCH_UPCOMING_CONTESTS_FAIL = 'FETCH_UPCOMING_CONTESTS_FAIL'
exports.UPCOMING_CONTESTS_FILTER_CHANGED = 'UPCOMING_CONTESTS_FILTER_CHANGED'
exports.SET_FOCUSED_CONTEST = 'SET_FOCUSED_CONTEST'
exports.UPCOMING_CONTESTS_ORDER_CHANGED = 'UPCOMING_CONTESTS_ORDER_CHANGED'

// reducers.upcoming-draft-groups-info
exports.FETCH_UPCOMING_DRAFTGROUPS_INFO = 'FETCH_UPCOMING_DRAFTGROUPS_INFO'
exports.FETCH_UPCOMING_DRAFTGROUPS_INFO_SUCCESS = 'FETCH_UPCOMING_DRAFTGROUPS_INFO_SUCCESS'
exports.FETCH_UPCOMING_DRAFTGROUPS_INFO_FAIL = 'FETCH_UPCOMING_DRAFTGROUPS_INFO_FAIL'

// reducers.lineups
exports.LINEUP_FOCUSED = 'LINEUP_FOCUSED'
exports.LINEUP_HOVERED = 'LINEUP_HOVERED'
exports.FETCH_UPCOMING_LINEUPS = 'FETCH_UPCOMING_LINEUPS'
exports.FETCH_UPCOMING_LINEUPS_FAIL = 'FETCH_UPCOMING_LINEUPS_FAIL'
exports.FETCH_UPCOMING_LINEUPS_SUCCESS = 'FETCH_UPCOMING_LINEUPS_SUCCESS'
exports.EDIT_LINEUP_INIT = 'EDIT_LINEUP_INIT'
exports.FILTER_UPCOMING_LINEUPS_BY_DRAFTGROUP_ID = 'FILTER_UPCOMING_LINEUPS_BY_DRAFTGROUP_ID'

// reducers.create-lineup
exports.SAVE_LINEUP_EDIT = 'SAVE_LINEUP_EDIT'
exports.CREATE_LINEUP_INIT = 'CREATE_LINEUP_INIT'
exports.CREATE_LINEUP_ADD_PLAYER = 'CREATE_LINEUP_ADD_PLAYER'
exports.CREATE_LINEUP_REMOVE_PLAYER = 'CREATE_LINEUP_REMOVE_PLAYER'
exports.CREATE_LINEUP_SAVE = 'CREATE_LINEUP_SAVE'
exports.CREATE_LINEUP_SAVE_FAIL = 'CREATE_LINEUP_SAVE_FAIL'
exports.CREATE_LINEUP_SET_TITLE = 'CREATE_LINEUP_SET_TITLE'
exports.CREATE_LINEUP_IMPORT = 'CREATE_LINEUP_IMPORT'

exports.ADD_CONTEST = 'ADD_CONTEST'
exports.REMOVE_CONTEST = 'REMOVE_CONTEST'
exports.UPDATE_CONTEST = 'UPDATE_CONTEST'

// reducers.current-box-scores
exports.MERGE_CURRENT_BOX_SCORES = 'MERGE_CURRENT_BOX_SCORES'
exports.UPDATE_CURRENT_BOX_SCORE = 'UPDATE_CURRENT_BOX_SCORE'

// reducers.current-lineups
exports.SET_CURRENT_LINEUPS = 'SET_CURRENT_LINEUPS'

// reducers.entries
exports.ADD_ENTRIES_PLAYERS = 'ADD_ENTRIES_PLAYERS'
exports.CONFIRM_RELATED_ENTRIES_INFO = 'CONFIRM_RELATED_ENTRIES_INFO'
exports.REQUEST_ENTRIES = 'REQUEST_ENTRIES'
exports.RECEIVE_ENTRIES = 'RECEIVE_ENTRIES'

// reducers.live
exports.LIVE_MODE_CHANGED = 'LIVE_MODE_CHANGED'

// reducers.live-contests
exports.CONFIRM_RELATED_LIVE_CONTEST_INFO = 'CONFIRM_RELATED_LIVE_CONTEST_INFO'
exports.REQUEST_LIVE_CONTEST_INFO = 'REQUEST_LIVE_CONTEST_INFO'
exports.RECEIVE_LIVE_CONTEST_INFO = 'RECEIVE_LIVE_CONTEST_INFO'
exports.REQUEST_LIVE_CONTEST_LINEUPS = 'REQUEST_LIVE_CONTEST_LINEUPS'
exports.RECEIVE_LIVE_CONTEST_LINEUPS = 'RECEIVE_LIVE_CONTEST_LINEUPS'
exports.UPDATE_LIVE_CONTEST_STATS = 'UPDATE_LIVE_CONTEST_STATS'

// reducers.live-draft-groups
exports.CONFIRM_LIVE_DRAFT_GROUP_STORED = 'CONFIRM_LIVE_DRAFT_GROUP_STORED'
exports.REQUEST_LIVE_DRAFT_GROUP_BOX_SCORES = 'REQUEST_LIVE_DRAFT_GROUP_BOX_SCORES'
exports.RECEIVE_LIVE_DRAFT_GROUP_BOX_SCORES = 'RECEIVE_LIVE_DRAFT_GROUP_BOX_SCORES'
exports.REQUEST_LIVE_DRAFT_GROUP_INFO = 'REQUEST_LIVE_DRAFT_GROUP_INFO'
exports.RECEIVE_LIVE_DRAFT_GROUP_INFO = 'RECEIVE_LIVE_DRAFT_GROUP_INFO'
exports.REQUEST_LIVE_DRAFT_GROUP_FP = 'REQUEST_LIVE_DRAFT_GROUP_FP'
exports.RECEIVE_LIVE_DRAFT_GROUP_FP = 'RECEIVE_LIVE_DRAFT_GROUP_FP'

// reducers.prizes
exports.REQUEST_PRIZE = 'REQUEST_PRIZE'
exports.RECEIVE_PRIZE = 'RECEIVE_PRIZE'

// reducers.transactions
exports.FETCH_TRANSACTIONS = 'FETCH_TRANSACTIONS'
exports.FETCH_TRANSACTIONS_SUCCESS = 'FETCH_TRANSACTIONS_SUCCESS'
exports.FETCH_TRANSACTIONS_FAIL = 'FETCH_TRANSACTIONS_FAIL'
exports.FILTER_TRANSACTIONS = 'FILTER_TRANSACTIONS'

// reducers.user
exports.FETCH_USER = 'FETCH_USER'
exports.FETCH_USER_FAIL = 'FETCH_USER_FAIL'
exports.FETCH_USER_SUCCESS = 'FETCH_USER_SUCCESS'

exports.UPDATE_USER_INFO = 'UPDATE_USER_INFO'
exports.UPDATE_USER_INFO_FAIL = 'UPDATE_USER_INFO_FAIL'
exports.UPDATE_USER_INFO_SUCCESS = 'UPDATE_USER_INFO_SUCCESS'

exports.UPDATE_USER_ADDRESS = 'UPDATE_USER_ADDRESS'
exports.UPDATE_USER_ADDRESS_FAIL = 'UPDATE_USER_ADDRESS_FAIL'
exports.UPDATE_USER_ADDRESS_SUCCESS = 'UPDATE_USER_ADDRESS_SUCCESS'

// reducers.payments
exports.FETCH_PAYMENTS = 'FETCH_PAYMENTS'
exports.FETCH_PAYMENTS_SUCCESS = 'FETCH_PAYMENTS_SUCCESS'
exports.FETCH_PAYMENTS_FAIL = 'FETCH_PAYMENTS_FAIL'
exports.ADD_PAYMENT_METHOD = 'ADD_PAYMENT_METHOD'
exports.ADD_PAYMENT_METHOD_SUCCESS = 'ADD_PAYMENT_METHOD_SUCCESS'
exports.ADD_PAYMENT_METHOD_FAIL = 'ADD_PAYMENT_METHOD_FAIL'
exports.SET_PAYMENT_METHOD_DEFAULT = 'SET_PAYMENT_METHOD_DEFAULT'
exports.SET_PAYMENT_METHOD_DEFAULT_SUCCESS = 'SET_PAYMENT_METHOD_SUCCESS'
exports.SET_PAYMENT_METHOD_DEFAULT_FAIL = 'SET_PAYMENT_METHOD_DEFAULT_FAIL'
exports.REMOVE_PAYMENT_METHOD = 'REMOVE_PAYMENT_METHOD'
exports.REMOVE_PAYMENT_METHOD_SUCCESS = 'REMOVE_PAYMENT_METHOD_SUCCESS'
exports.REMOVE_PAYMENT_METHOD_FAIL = 'REMOVE_PAYMENT_METHOD_FAIL'
exports.WITHDRAW_AMOUNT = 'WITHDRAW'
exports.WITHDRAW_AMOUNT_FAIL = 'WITHDRAW_FAIL'
exports.WITHDRAW_AMOUNT_SUCCESS = 'WITHDRAW_SUCCESS'
exports.DEPOSIT_AMOUNT = 'DEPOSIT'
exports.DEPOSIT_AMOUNT_FAIL = 'DEPOSIT_FAIL'
exports.DEPOSIT_AMOUNT_SUCCESS = 'DEPOSIT_SUCCESS'

// reducers.results
exports.REQUEST_LINEUPS_RESULTS = 'REQUEST_LINEUPS_RESULTS'
exports.RECEIVE_LINEUPS_RESULTS = 'RECEIVE_LINEUPS_RESULTS'
