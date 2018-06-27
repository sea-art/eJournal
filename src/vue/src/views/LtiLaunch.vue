<template>
    <content-single-columns>
        <h1 class="title-container">{{ currentPage }}</h1>
        <lti-create-connect-course v-if="handleCourseChoice" @handleAction="handleActions" :lti="lti"/>
        <lti-create-connect-assignment v-else-if="handleAssignmentChoice" @handleAction="handleActions" :lti="lti" :page="page"/>
        <lti-create-assignment v-else-if="createAssignment" @handleAction="handleActions" :lti="lti" :page="page"/>
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
            currentPage: 'LTI Integration',

            /* Variables for loading the right component. */
            handleCourseChoice: false,
            handleAssignmentChoice: false,
            createAssignment: false,

            /* Possible states for the control flow. */
            states: {
                state: '',

                /* Extern variables for checking the state of the lti launch. */
                bad_auth: '-1',
                no_course: '0',
                no_assign: '1',
                new_course: '2',
                new_assign: '3',
                finish_t: '4',
                finish_s: '5',
                grade_center: '6',

                /* Intern variables for checking the state of the lti launch. */
                create_assign: '7',
                check_assign: '8'
            },

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
        handleActions (args) {
            switch (args[0]) {
            case 'courseCreated':
                this.handleCourseChoice = false
                this.page.cID = args[1]
                this.states.state = this.states.create_assign
                alert('Course Created!')
                break
            case 'courseConnected':
                this.handleCourseChoice = false
                this.page.cID = args[1]
                this.states.state = this.states.check_assign
                alert('Course Connected!')
                break
            case 'assignmentIntegrated':
                this.handleAssignmentChoice = false
                this.states.state = this.states.finish_t
                alert('Assignment Integrated!')
                break
            case 'assignmentCreated':
                this.createAssignment = false
                this.page.aID = args[1]
                this.states.state = this.states.finish_t
                alert('Assignment Created!')
                break
            }
        },
        updateState (state) {
            switch (state) {
            case this.states.new_course:
                this.currentPage = 'Course Integration'
                this.handleCourseChoice = true
                break
            case this.states.new_assign:
                this.currentPage = 'Assignment Integration'
                this.handleAssignmentChoice = true
                break
            case this.states.create_assign:
                this.currentPage = 'Assigment Integration'
                this.createAssignment = true
                break
            case this.states.check_assign:
                assignApi.get_assignment_by_lti_id(this.lti.ltiAssignID)
                    .then(response => {
                        if (response === undefined) {
                            this.states.state = this.states.new_assign
                        } else {
                            this.page.aID = response.aID
                            this.states.state = this.states.finish_t
                        }
                    })
                break
            case this.states.grade_center:
                this.$router.push({
                    name: 'Journal',
                    params: {
                        cID: this.page.cID,
                        aID: this.page.aID,
                        jID: this.page.jID
                    }
                })
                break
            }
        }
    },
    watch: {
        state: function (val) {
            if (val === this.states.finish_s) {
                this.$router.push({
                    name: 'Journal',
                    params: {
                        cID: this.page.cID,
                        aID: this.page.aID,
                        jID: this.page.jID
                    }
                })
            } else if (val === this.states.finish_t) {
                this.$router.push({
                    name: 'Assignment',
                    params: {
                        cID: this.page.cID,
                        aID: this.page.aID
                    }
                })
            } else {
                this.updateState(this.states.state)
            }
        }
    },
    mounted () {
        /* Get the lti information from the query. */
        this.lti.ltiCourseID = this.$route.query.lti_cID
        this.lti.ltiCourseName = this.$route.query.lti_cName
        this.lti.ltiCourseAbbr = this.$route.query.lti_abbr
        this.states.state = this.$route.query.state

        this.lti.ltiAssignName = this.$route.query.lti_aName
        this.lti.ltiAssignID = this.$route.query.lti_aID
        this.lti.ltiPointsPossible = this.$route.query.lti_points_possible

        this.page.cID = this.$route.query.cID
        this.page.aID = this.$route.query.aID
        this.page.jID = this.$route.query.jID

        if (this.states.state === this.states.bad_auth) {
            this.$router.push({
                name: 'ErrorPage',
                params: {
                    errorCode: '511',
                    errorMessage: 'Network authorization required'
                }
            })
        } else if (this.states.state === this.states.no_course) {
            this.$router.push({
                name: 'ErrorPage',
                params: {
                    errorCode: '404',
                    errorMessage: 'No course found with given ID'
                }
            })
        } else if (this.states.state === this.states.no_assign) {
            this.$router.push({
                name: 'ErrorPage',
                params: {
                    errorCode: '404',
                    errorMessage: 'No assignment found with given ID'
                }
            })
        } else {
            this.updateState(this.states.state)
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
