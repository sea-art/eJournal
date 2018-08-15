import Vue from 'vue'
import Vuex from 'vuex'
// import createPersistedState from 'vuex-persistedstate'

import user from './modules/user'

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== 'production'
// const plugins = []

// plugins.push(createPersistedState({ paths: ['user', 'permissions'] }))

export default new Vuex.Store({
    modules: {
        user
    },
    strict: debug
    // plugins
})
