import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'flatpickr/dist/flatpickr.css' // eslint-disable-line import/no-extraneous-dependencies
import 'intro.js/introjs.css'

import '@/helpers/vue_awesome_icons.js'
import initSentry from '@/helpers/sentry.js'
import CKEditor from '@ckeditor/ckeditor5-vue'

import Toasted from 'vue-toasted'
import flatPickr from 'vue-flatpickr-component'
import VueIntro from 'vue-introjs'
import Icon from 'vue-awesome/components/Icon.vue'
import VueMoment from 'vue-moment'

import App from './App.vue'
import router from './router'
import store from './store'
import ThemeSelect from './components/assets/ThemeSelect.vue'

import connection from '@/api/connection.js'
import authImage from '@/helpers/auth_image.js'

Vue.config.productionTip = false
Vue.use(Toasted, { position: 'top-center', duration: 4000 })
Vue.use(BootstrapVue)
Vue.use(flatPickr)
Vue.use(VueIntro)
Vue.use(VueMoment)
Vue.use(CKEditor)
Vue.use(authImage)

Vue.component('icon', Icon)
Vue.component('theme-select', ThemeSelect)

initSentry(Vue)

/* Checks the store for for permissions according to the current route cID or aID. */
Vue.prototype.$hasPermission = store.getters['permissions/hasPermission']
const toApi = new RegExp(`^${CustomEnv.API_URL}`)

Vue.config.productionTip = false

/* eslint-disable */
;(function (open, send) {
    let xhrOpenRequestUrl

    XMLHttpRequest.prototype.open = function (_, url) {
        xhrOpenRequestUrl = url
        open.apply(this, arguments)
    }

    XMLHttpRequest.prototype.send = function () {
        if (store.getters['user/jwtAccess'] && toApi.test(xhrOpenRequestUrl)) {
            this.setRequestHeader('Authorization', `Bearer ${store.getters['user/jwtAccess']}`)
        }
        send.apply(this, arguments)
    }
})(XMLHttpRequest.prototype.open, XMLHttpRequest.prototype.send)
/* eslint-enable */

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
        maxFileSizeBytes: 10485760,
        maxEmailFileSizeBytes: 10485760,
        flatPickrTimeConfig: {
            enableTime: true,
            time_24hr: true,
            defaultHour: 23,
            defaultMinute: 59,
            altInput: true,
            altFormat: 'D d M Y H:i',
            dateFormat: 'Y-m-dTH:i:S',
        },
        flatPickrConfig: {
            enableTime: false,
            altInput: true,
            altFormat: 'D d M Y',
            dateFormat: 'Y-m-d',
        },
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
        lgMax () { return this.windowWidth < 1200 },
    },
    created () {
        store.dispatch('connection/setupConnectionInterceptors', { connection: connection.conn })
        store.dispatch('connection/setupConnectionInterceptors',
            { connection: connection.connRefresh, isRefresh: true })
        store.dispatch('connection/setupConnectionInterceptors', { connection: connection.connFile })
        store.dispatch('connection/setupConnectionInterceptors', { connection: connection.connFileEmail })

        window.addEventListener('resize', () => {
            this.windowWidth = window.innerWidth
        })
        this.windowWidth = window.innerWidth
    },
    methods: {
        getBorderClass (cID) {
            return this.colors[cID % this.colors.length]
        },
        beautifyDate (date, displayDate = true, displayTime = true) {
            if (!date) {
                return ''
            }
            const year = date.substring(0, 4)
            const month = date.substring(5, 7)
            const day = date.substring(8, 10)
            const time = date.substring(11, 16)
            let s = ''
            if (displayDate) {
                s += `${day}-${month}-${year}`
            }
            if (displayDate && displayTime) {
                s += ' at '
            }
            if (displayTime) {
                s += time
            }
            return s
        },
    },
    render: h => h(App),
    template: '<App/>',
}).$mount('#app')
