import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

import user from './modules/user'
import permissions from './modules/permissions'
import connection from './modules/connection'
import preferences from './modules/preferences'

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== 'production'
const plugins = []

plugins.push(createPersistedState({ paths: ['user', 'permissions', 'preferences'] }))

export default new Vuex.Store({
    modules: {
        user,
        permissions,
        connection,
        preferences,
    },
    strict: debug,
    plugins,
})
