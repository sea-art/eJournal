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
import 'vue-awesome/icons/plus-square'
import 'vue-awesome/icons/hourglass-half'
import 'vue-awesome/icons/check'
import 'vue-awesome/icons/times'
import 'vue-awesome/icons/exclamation'
import 'vue-awesome/icons/plus'
import 'vue-awesome/icons/list-ul'

import Toasted from 'vue-toasted'
import TinyMCE from '@tinymce/tinymce-vue'

Vue.config.productionTip = false
Vue.use(Toasted, { position: 'bottom-right', duration: 4000 })
Vue.use(BootstrapVue)

Vue.component('tiny-mce', TinyMCE)

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    components: { App },
    data: {
        colors: ['pink-border', 'peach-border', 'blue-border'],
        permissions: {},
        validToken: false,
        previousPage: null,
        windowWidth: 0
    },
    mounted () {
        this.$nextTick(function () {
            window.addEventListener('resize', this.getWindowWidth)

            this.getWindowWidth()
        })
    },
    beforeDestroy () {
        window.removeEventListener('resize', this.getWindowWidth)
    },
    methods: {
        getWindowWidth () {
            this.windowWidth = window.innerWidth
        },
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
        timeLeft (date) {
            /* Date format is:
             * Returns the remaining time left as:
             * If the time left is negative returns Expired
             * TODO implement (will most likely require a lib) */
            return '1M 9D 9H'
        },
        getBorderClass (cID) {
            return this.colors[cID % this.colors.length]
        },

        /* #############################################################
         *              Permissions,
         * Front-end interface for all possible permissions.
         * For an overview see:
         * https://docs.google.com/spreadsheets/d/1M7KnEKL3cG9PMWfQi9HIpRJ5xUMou4Y2plnRgke--Tk
         *
         * ##############################################################
         */

        /* Site-wide permissions */
        isAdmin () {
            return this.permissions.is_superuser
        },
        /* Institute wide settings, think institute name/abbreviation logo. */
        canEditInstitute () {
            return this.permissions.can_edit_institute
        },

        /* Course level based permissions. These permissions are enabled and
        used per course. */

        /* Course permissions. */
        canEditCourseRoles () {
            return this.permissions.can_edit_course_roles
        },
        canAddCourse () {
            return this.permissions.can_add_course
        },
        canViewCourseParticipants () {
            return this.permissions.can_view_course_participants
        },
        canAddCourseParticipants () {
            return this.permissions.can_add_course_participants
        },
        canEditCourse () {
            return this.permissions.can_edit_course
        },
        canDeleteCourse () {
            return this.permissions.can_delete_course
        },

        /* Assignment permissions. */
        canAddAssignment () {
            return this.permissions.can_add_assignment
        },
        canEditAssignment () {
            return this.permissions.can_edit_assignment
        },
        canViewAssignmentParticipants () {
            return this.permissions.can_view_assignment_participants
        },
        canDeleteAssignment () {
            return this.permissions.can_delete_assignment
        },
        canPublishAssignmentGrades () {
            return this.permissions.can_publish_assignment_grades
        },

        /* Grade permissions. */
        canGradeJournal () {
            return this.permissions.can_grade_journal
        },
        canPublishJournalGrades () {
            return this.permissions.can_publish_journal_grades
        },
        canEditJournal () {
            return this.permissions.can_edit_journal
        },
        canCommentJournal () {
            return this.permissions.can_comment_journal
        }
    },
    template: '<App/>'
})
