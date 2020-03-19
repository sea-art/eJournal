import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

import connection from './modules/connection'
import content from './modules/content'
import permissions from './modules/permissions'
import preferences from './modules/preferences'
import sentry from './modules/sentry'
import user from './modules/user'

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== 'production'
const plugins = []

plugins.push(createPersistedState({ paths: ['content', 'permissions', 'preferences', 'user'] }))

export default new Vuex.Store({
    modules: {
        connection,
        content,
        permissions,
        preferences,
        sentry,
        user,
    },
    strict: debug,
    plugins,
})
