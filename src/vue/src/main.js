import Vue from 'vue'
import App from './App'
import router from './router'
import BootstrapVue from 'bootstrap-vue'
import '../node_modules/bootstrap/dist/css/bootstrap.css'
import '../node_modules/bootstrap-vue/dist/bootstrap-vue.css'
import 'vue-awesome/icons/eye'
import 'vue-awesome/icons/caret-up'
import 'vue-awesome/icons/caret-down'
import 'vue-awesome/icons/arrows'
import 'vue-awesome/icons/trash'

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

        /* #############################################################
         *              Permissions, for overview see:
         *
         * https://docs.google.com/spreadsheets/d/1M7KnEKL3cG9PMWfQi9HIpRJ5xUMou4Y2plnRgke--Tk/edit?usp=sharing
         *
         * ##############################################################
         */

        /* The admin has all permissions. Extra, site-wide permissions:
         * Creating a course on the home page
         * Editing institution-wide settings
         * Editing someone else profile (picture) */
        isAdmin () {
            return this.permissions.is_admin
        },
        /* Insitutue wide settings, think institute name/abbreviation logo. */
        canEditInstitute () {
            // TODO API
            return true
        },


        /* Course level based permissions. These permissions are enabled and
        used per course. */
        /* Course permissions. */
        canViewCourseParticipants () {
            // TODO API
            return true
        },
        /* Note that teachers can add courses as well, no cID available yet.
         * Required for LTI integration. */
        canAddCourse () {
            // TODO API
            return true
        },
        canEditCourse () {
            return this.permissions.can_edit_course
        },
        canEditCourseRoles () {
            // TODO API
            return true
        },
        canDeleteCourse () {
            return this.permissions.can_delete_course
        },

        /* Assignment permissions. */
        canViewCourseParticipants () {
            // TODO Change backend confusing name
            return this.permissions.can_view_assignment
        },
        canAddAssignment () {
            // TODO Streamline backend name
            return this.permissions.can_submit_assignment
        },
        canEditAssignment () {
            return this.permissions.can_edit_assignment
        },
        canDeleteAssignment () {
            return this.permissions.can_delete_assignment
        },
        canPublishAssignmentGrades () {
            // TODO API
            return true
        },

        /* Journal level permissions */
        canGradeJournal () {
            // TODO API
            return true
        },
        canPublishJournalGrades () {
            // TODO API
            return true
        },
        canEditJournal () {
            // TODO API
            return true
        },
        canCommentJournal () {
            // TODO API
            return true
        }
    },
    template: '<App/>'
})
