<template>
    <content-single-columns>
        <b-modal
            slot="main-content-column"
            ref="chooseActionRef"
            title="Choose LTI integration method"
            size="lg"
            hide-footer>
                <lti-create-connect @handleAction="handleConfirm('chooseActionRef')"></lti-create-connect>
        </b-modal>

        <b-modal
            slot="main-content-column"
            ref="createCourseRef"
            title="Create course"
            size="lg"
            hide-footer>
                <create-course @handleAction="handleConfirm('createCourseRef')"></create-course>
        </b-modal>
    </content-single-columns>
</template>

<script>
import contentSingleColumn from '@/components/ContentSingleColumn.vue'
import createCourse from '@/components/CreateCourse.vue'
import ltiCreateConnect from '@/components/LtiCreateConnect.vue'

export default {
    name: 'LtiLaunch',
    components: {
        'content-single-columns': contentSingleColumn,
        'create-course': createCourse,
        'lti-create-connect': ltiCreateConnect
    },
    data () {
        return {
            msg: 'unsuccesfull',
            jwt_refresh: ':(',
            chooseAction: '',

            /* Variables for checking the state of the lti launch. */
            s_new_course: '0',
            s_new_assignment: '1',
            s_finish: '2',
            s_finish_student: '3'
        }
    },
    methods: {
        showModal (ref) {
            this.$refs[ref].show()
        },
        hideModal (ref) {
            this.$refs[ref].hide()
        },
        handleConfirm (ref, m) {
            this.hideModal(ref)
            alert(m)

            if (ref === 'chooseActionRef') {

            }
        }
    },
    mounted () {
        if (localStorage.getItem('jwt_access') === null) {
            localStorage.setItem('jwt_access', this.$route.query.jwt_access)
        }

        if (localStorage.getItem('jwt_refresh') === null) {
            localStorage.setItem('jwt_refresh', this.$route.query.jwt_refresh)
        }

        this.msg = this.$route.query.jwt_access
        this.jwt_refresh = this.$route.query.jwt_refresh

        /* Get the IDs of the objects out of the query. */
        var ltiCourseID = this.$route.query.lti_cID
        var ltiCourseName = this.$route.query.lti_cName
        var ltiCourseAbbr = this.$route.query.lti_abbr
        var role = this.$route.query.role
        var state = this.$route.query.state

        var ltiAssignName = this.$route.query.lti_aName
        var ltiAssignID = this.$route.query.lti_aID
        var ltiPointsPossible = this.$route.query.lti_points_possible

        var cID = this.$route.query.cID
        var aID = this.$route.query.aID
        var jID = this.$route.query.jID

        alert(state === this.s_new_course)

        if (role === 'ta' || role === 'teacher') {
            if (state === this.s_new_course) {
                // TODO Create or koppel assignement
                this.showModal('chooseActionRef')
            } else if (state === this.s_new_assignment) {
                // TODO Create or koppel assignement
            } else if (state === this.s_finish) {
                this.$router.push({
                    name: 'Assignment',
                    params: {
                        cID: cID,
                        aID: aID
                    }
                })
            } else {
                // TODO Something went wrong -> 404 // should not be possible
                this.$router.push({
                    name: 'ErrorPage'
                })
            }
        } else if (role === 'student') {
            if (state === this.s_finish_student) {
                this.$router.push({
                    name: 'Journal',
                    params: {
                        cID: cID,
                        aID: aID,
                        jID: jID
                    }
                })
            } else if (state === this.s_new_course) {
                // TODO 404 course not found
                this.$router.push({
                    name: 'ErrorPage'
                })
            } else if (state === this.s_new_assignment) {
                // TODO 404 assignment not found
                this.$router.push({
                    name: 'ErrorPage'
                })
            } else {
                // TODO should not be possible
            }
        }
    }
}
</script>
