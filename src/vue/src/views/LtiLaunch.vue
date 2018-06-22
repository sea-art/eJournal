<template>
    <content-single-columns>
        <h1 class="title-container">{{ currentPage }}</h1>
        <lti-create-connect-course v-if="handleCourseChoice" @handleAction="handleActions" :lti="lti"/>
        <lti-create-connect-assignment v-if="handleAssignmentChoice" @handleAction="handleActions"/>
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
            currentPage: 'LTI Integration',

            /* Variables for loading the right component. */
            handleCourseChoice: false,
            handleAssignmentChoice: false,
            createCourse: false,
            connectCourse: false,
            createAssignment: false,
            connectAssignment: false,

            /* Extern variables for checking the state of the lti launch. */
            state: '',
            s_bad_auth: '-1',
            s_no_course: '0',
            s_no_assign: '1',
            s_new_course: '2',
            s_new_assign: '3',
            s_finish_t: '4',
            s_finish_s: '5',

            /* Intern variables for checking the state of the lti launch. */
            s_create_assign: '6',
            s_check_assign: '7',

            /* Set a dictionary with the needed lti variables. */
            lti: {
                ltiCourseID: '',
                ltiCourseName: '',
                ltiCourseAbbr: ''
            }
        }
    },
    methods: {
        handleActions (msg) {
            if (msg === 'courseCreated') {
                this.handleCourseChoice = false
                this.state = this.s_create_assign
                alert('Course Created!')
            } else if (msg === 'courseConnected') {
                this.handleCourseChoice = false
                this.state = this.s_check_assign
                alert('Course Connected!')
            } else if (msg === 'assignementIntegrated') {
                this.handleAssignmentChoice = false
                this.state = this.s_finish_t
                alert('Assignment Integrated!')
            }
        },
        updateState (state) {
            switch (state) {
                case this.s_new_course:
                    this.currentPage = 'Course Integration'
                    this.handleCourseChoice = true
                    break;
                case this.s_new_assign:
                    this.currentPage = 'Assignment Integration'
                    this.handleAssignmentChoice = true
                    break;
                case this.s_create_assign:
                    // TODO: Maak nieuwe assignement aan
                    break;
                case this.s_check_assign:
                    // TODO: Check if assignment already exists
                    break;
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
        this.ltiCourseID = this.$route.query.lti_cID
        this.ltiCourseName = this.$route.query.lti_cName
        this.ltiCourseAbbr = this.$route.query.lti_abbr
        this.state = this.$route.query.state

        var ltiAssignName = this.$route.query.lti_aName
        var ltiAssignID = this.$route.query.lti_aID
        var ltiPointsPossible = this.$route.query.lti_points_possible

        var cID = this.$route.query.cID
        var aID = this.$route.query.aID
        var jID = this.$route.query.jID

        this.state = '0'

        if (this.state === this.s_bad_auth) {
            // TODO: There was a bad LTI request. Give correct error.
        } else if (this.state === this.s_no_course || this.state === this.s_no_course) {
            // TODO: There is no course/assignment availible. Give correct error.
        } else {
            while (this.state !== this.s_finish_s || this.state !== this.s_finish_t)  {
                this.state = this.updateState(this.state)
            }
        }

        //         this.$router.push({
        //             name: 'Journal',
        //             params: {
        //                 cID: cID,
        //                 aID: aID,
        //                 jID: jID
        //             }
        //         })
    }
}
</script>

<style>
.title-container {
    padding-right: 10px;
    padding-bottom: 12px;
    margin-bottom: -4px;
}

@media(max-width:992px) {
    .title-container  {
        padding-top: 12px !important;
        margin-top: -4px !important;
    }
}
</style>
