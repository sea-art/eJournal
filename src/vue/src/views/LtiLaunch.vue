<template>
    <content-single-columns>
        <h1 class="title-container">{{ currentPage }}</h1>
        <lti-create-connect-course v-if="handleCourseChoice" @handleAction="handleActions" :lti="lti"/>
        <lti-create-connect-assignment v-else-if="handleAssignmentChoice" @handleAction="handleActions"/>
        <lti-create-assignment v-else-if="createAssignment" @handleAction="handleActions"/>
    </content-single-columns>
</template>

<script>
import contentSingleColumn from '@/components/ContentSingleColumn.vue'
import ltiCreateConnectCourse from '@/components/LtiCreateConnectCourse.vue'
import ltiCreateConnectAssignment from '@/components/LtiCreateConnectAssignment.vue'
import ltiCreateAssignment from '@/components/LtiCreateAssignment.vue'
import assignApi from '@/api/assignment.js'

export default {
    name: 'LtiLaunch',
    components: {
        'content-single-columns': contentSingleColumn,
        'lti-create-connect-course': ltiCreateConnectCourse,
        'lti-create-connect-assignment': ltiCreateConnectAssignment,
        'lti-create-assignment': ltiCreateAssignment
    },
    data () {
        return {
            msg: 'unsuccesfull',
            jwt_refresh: ':(',
            currentPage: 'LTI Integration',

            /* Variables for loading the right component. */
            handleCourseChoice: false,
            handleAssignmentChoice: false,
            createAssignment: false,

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
                ltiCourseAbbr: '',
                ltiAssignName: '',
                ltiAssignID: '',
                ltiPointsPossible: ''
            },

            /* Set a dictionary with the variables of the linked page. */
            page: {
                cID: '',
                aID: '',
                jID: ''
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
            } else if (msg === 'assignmentCreated') {
                this.createAssignment = false
                this.state = this.s_finish_t
                alert('Assignment Created!')
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
                    this.currentPage = 'Assigment Integration'
                    this.createAssignment = true
                    break;
                case this.s_check_assign:
                    assignApi.get_assignment_by_lti_id(this.lti.ltiAssignID)
                        .then(response => {
                            if (response === undefined)
                                this.state = this.s_new_assign
                            else {
                                this.page.aID = response.aID
                                this.state = this.s_finish_t
                            }
                        })
                    break;
            }
        }
    },
    watch: {
        state: function (val) {
            if (val !== this.s_finish_s && val !== this.s_finish_t)
                this.updateState(this.state)
            else if (val === this.s_finish_s) {
                this.$router.push({
                    name: 'Journal',
                    params: {
                        cID: this.page.cID,
                        aID: this.page.aID,
                        jID: this.page.jID
                    }
                })
            } else if (val === this.s_finish_t) {
                this.$router.push({
                    name: 'Assignment',
                    params: {
                        cID: this.page.cID,
                        aID: this.page.aID
                    }
                })
            }
        }
    },
    mounted () {
        if (this.$route.query.jwt_access !== undefined)
            localStorage.setItem('jwt_access', this.$route.query.jwt_access)

        if (this.$route.query.jwt_refresh !== undefined)
            localStorage.setItem('jwt_refresh', this.$route.query.jwt_refresh)

        /* Get the IDs of the objects out of the query. */
        this.lti.ltiCourseID = this.$route.query.lti_cID
        this.lti.ltiCourseName = this.$route.query.lti_cName
        this.lti.ltiCourseAbbr = this.$route.query.lti_abbr
        this.state = this.$route.query.state

        this.lti.ltiAssignName = this.$route.query.lti_aName
        this.lti.ltiAssignID = this.$route.query.lti_aID
        this.lti.ltiPointsPossible = this.$route.query.lti_points_possible

        this.page.cID = this.$route.query.cID
        this.page.aID = this.$route.query.aID
        this.page.jID = this.$route.query.jID

        this.state = '2'

        if (this.state === this.s_bad_auth) {
            this.$router.push({
                name: 'ErrorPage',
                params: {
                    errorCode: '511',
                    errorMessage: 'Network authorization required'
                }
            })
        } else if (this.state === this.s_no_course) {
            this.$router.push({
                name: 'ErrorPage',
                params: {
                    errorCode: '404',
                    errorMessage: 'No course found with given ID'
                }
            })
        } else if (this.state === this.s_no_assign) {
            this.$router.push({
                name: 'ErrorPage',
                params: {
                    errorCode: '404',
                    errorMessage: 'No assignment found with given ID'
                }
            })
        } else {
            this.updateState(this.state)
        }
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
