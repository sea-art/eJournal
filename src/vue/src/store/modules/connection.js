import * as types from '../constants/mutation-types.js'

const getters = {
    openApiCalls: state => state.openApiCalls,
    checkOpenApiCalls: state => state.openApiCalls > 0,
}

const mutations = {
    [types.CLOSE_API_CALL] (state) {
        state.openApiCalls--
    },
    [types.OPEN_API_CALL] (state) {
        state.openApiCalls++
    },
}

export default {
    namespaced: true,
    state: {
        openApiCalls: 0,
    },
    getters,
    mutations,
}
