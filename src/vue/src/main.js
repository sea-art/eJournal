import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import axios from 'axios'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'flatpickr/dist/flatpickr.css'
import 'intro.js/introjs.css'

import '@/helpers/vue-awesome-icons.js'

import Toasted from 'vue-toasted'
import flatPickr from 'vue-flatpickr-component'
import VueIntro from 'vue-introjs'
import VueMoment from 'vue-moment'

Vue.config.productionTip = false
Vue.use(Toasted, { position: 'top-center', duration: 4000 })
Vue.use(BootstrapVue)
Vue.use(flatPickr)
Vue.use(VueIntro)
Vue.use(VueMoment)

/* Checks the store for for permissions according to the current route cID or aID. */
Vue.prototype.$hasPermission = store.getters['permissions/hasPermission']

/* Sets the default authorization token needed to for authenticated requests. */
axios.defaults.transformRequest.push((data, headers) => {
    if (store.getters['user/jwtAccess']) {
        headers.Authorization = 'Bearer ' + store.getters['user/jwtAccess']
    }
    return data
})

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    store,
    components: { App },
    data: {
        colors: ['pink-border', 'purple-border', 'yellow-border', 'blue-border'],
        previousPage: null,
        windowWidth: 0,
        maxFileSizeBytes: 5242880,
        maxEmailFileSizeBytes: 10485760,
        flatPickrTimeConfig: {
            enableTime: true,
            time_24hr: true,
            defaultHour: 23,
            defaultMinute: 59
        }
    },
    created () {
        window.addEventListener('resize', () => {
            this.windowWidth = window.innerWidth
        })
        this.windowWidth = window.innerWidth
    },
    computed: {
        /* Bootstrap breakpoints for custom events. */
        // TODO Figure out how to get these from the dedicated sass file (more webpack fun)
        sm () { return this.windowWidth > 575 },
        md () { return this.windowWidth > 767 },
        lg () { return this.windowWidth > 991 },
        xl () { return this.windowWidth > 1199 },
        xsMax () { return this.windowWidth < 576 },
        smMax () { return this.windowWidth < 769 },
        mdMax () { return this.windowWidth < 992 },
        lgMax () { return this.windowWidth < 1200 }
    },
    methods: {
        getBorderClass (cID) {
            return this.colors[cID % this.colors.length]
        },
        beautifyDate (date, displayDate = true, displayTime = true) {
            if (!date) {
                return ''
            }
            var year = date.substring(0, 4)
            var month = date.substring(5, 7)
            var day = date.substring(8, 10)
            var time = date.substring(11, 16)
            var s = ''
            if (displayDate) {
                s += day + '-' + month + '-' + year
            }
            if (displayDate && displayTime) {
                s += ' at '
            }
            if (displayTime) {
                s += time
            }
            return s
        }
    },
    template: '<App/>'
})
