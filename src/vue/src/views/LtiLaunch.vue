<template>
    <content-single-columns>
        <lti-create-connect-course v-if="handleCourseChoice" slot="main-content-column" @handleAction="handleActions"/>
        <lti-create-connect-assignment v-if="handleAssignmentChoice" slot="main-content-column" @handleAction="handleActions"/>
    </content-single-columns>
</template>

<script>
import contentSingleColumn from '@/components/ContentSingleColumn.vue'
import ltiCreateConnectCourse from '@/components/LtiCreateConnectCourse.vue'
import ltiCreateConnectAssignment from '@/components/LtiCreateConnectAssignment.vue'

export default {
    name: 'LtiLaunch',
    components: {
        'content-single-columns': contentSingleColumn,
        'lti-create-connect-course': ltiCreateConnectCourse,
        'lti-create-connect-assignment': ltiCreateConnectAssignment
    },
    data () {
        return {
            msg: 'unsuccesfull',
            jwt_refresh: ':(',

            /* Variables for loading the right component. */
            handleCourseChoice: false,
            handleAssignmentChoice: false,
            createCourse: false,
            connectCourse: false,
            createAssignment: false,
            connectAssignment: false,

            /* Variables for checking the state of the lti launch. */
            s_new_course: '0',
            s_new_assignment: '1',
            s_finish: '2',
            s_finish_student: '3'
        }
    },
    methods: {
        handleActions (msg) {
            this.handleChoice = false

            if (msg === 'courseIntegrated') {
                alert('Course Integrated!')
            } else {
                alert('Iets anders gebeurd!')
            }
        }
    },
    mounted () {
        if (this.$route.query.jwt_access !== undefined) {
            localStorage.setItem('jwt_access', this.$route.query.jwt_access)
        }

        if (this.$route.query.jwt_refresh !== undefined) {
            localStorage.setItem('jwt_refresh', this.$route.query.jwt_refresh)
        }

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

        // alert(state === this.s_new_course)
        state = '0'
        role = 'ta'
        alert('State: ' + state + '\nRole: ' + role)

        if (role === 'ta' || role === 'teacher') {
            if (state === this.s_new_course) {
                alert('hi')
                this.handleCourseChoice = true
                // TODO Create or koppel assignement

                // this.showModal('chooseActionRef')
            } else if (state <= this.s_new_assignment) {
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
