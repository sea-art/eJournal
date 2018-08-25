import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

import user from './modules/user'
import permissions from './modules/permissions'

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== 'production'
const plugins = []

plugins.push(createPersistedState({ paths: ['user', 'permissions'] }))

export default new Vuex.Store({
    modules: {
        user,
        permissions
    },
    strict: debug,
    plugins
})
