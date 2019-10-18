import * as Sentry from '@sentry/browser'
import * as types from '../constants/mutation-types.js'

const getters = {
    lastEvenID: state => state.lastEvenID,
}

const mutations = {
    [types.SET_LAST_EVENT_ID] (state, { eventID }) {
        state.lastEvenID = eventID
    },
    [types.SET_SENTRY_USER_SCOPE] (state, data) { // eslint-disable-line
        Sentry.configureScope((scope) => {
            scope.setUser({
                id: data.uID,
            })
        })
    },
    [types.RESET_SENTRY] (state) {
        state.lastEvenID = null
        Sentry.configureScope((scope) => {
            scope.clear()
        })
    },
}

export default {
    namespaced: true,
    state: {
        lastEvenID: null,
    },
    getters,
    mutations,
}
