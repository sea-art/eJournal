import * as types from '../constants/mutation-types.js'

const getters = {
    lastEvenID: state => state.lastEvenID,
}

const mutations = {
    [types.SET_LAST_EVENT_ID] (state, { eventID }) {
        state.lastEvenID = eventID
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
