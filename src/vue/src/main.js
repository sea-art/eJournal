import Vue from 'vue'
import App from './App'
import router from './router'
import BootstrapVue from 'bootstrap-vue'
import '../node_modules/bootstrap/dist/css/bootstrap.css'
import '../node_modules/bootstrap-vue/dist/bootstrap-vue.css'
import 'vue-awesome/icons/eye'
import 'vue-awesome/icons/caret-up'
import 'vue-awesome/icons/caret-down'

Vue.config.productionTip = false
Vue.use(BootstrapVue)

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    components: { App },
    data: {
        colors: ['pink-border', 'peach-border', 'blue-border'],
        permissions: {},
        validToken: false
    },
    methods: {
        timeLeft (date) {
            /* Date format is:
             * Returns the remaining time left as:
             * If the time left is negative returns Expired
             * TODO implement (will most likely require a lib) */
            return '1M 9D 9H'
        },
        /* Admin has all permissions, including the ones listed below plus:
         * Creating a course
         * Editing institute wide settings */
        isAdmin () {
            return this.permissions.is_admin
        },

        /* Course level based permissions. */
        canEditCourse () {
            return this.permissions.can_edit_course
        },
        canDeleteCourse () {
            return this.permissions.can_delete_course
        },

        /* Assigment level base permissions. */
        canViewAssigment () {
            return this.permissions.can_view_assignment
        },
        canSubmitAssignment () {
            return this.permissions.can_submit_assignment
        },
        canEditAssignment () {
            return this.permissions.can_edit_assignment
        },
        canDeleteAssignment () {
            return this.permissions.can_delete_assignment
        },

        /* Grade based permissions. */
        canViewGrades () {
            return this.permissions.can_view_grades
        },
        canEditGrades () {
            return this.permissions.can_edit_grades
        }
    },
    template: '<App/>'
})
