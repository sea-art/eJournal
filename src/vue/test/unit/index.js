import Vue from 'vue'

import BootstrapVue from 'bootstrap-vue'
import '../../node_modules/bootstrap/dist/css/bootstrap.css'
import '../../node_modules/bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)
Vue.config.productionTip = false

// require all test files (files that ends with .spec.js)
const testsContext = require.context('./specs', true, /\.spec$/)
testsContext.keys().forEach(testsContext)

// require all src files except main.js for coverage.
// you can also change this to match only the subset of files that
// you want coverage for.

// TODO Set proper subsets of files to test add handler for md and sass, currently
// All files are tested pointlessly

/* Skips main.js, *.sass *.md */
// const srcContext = require.context('../../src', true, /^\.\/(?!(main(\.js)?$)|.*(\.sass)$|.*(\.md)$)/)
// srcContext.keys().forEach(srcContext)
