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
import ltiApi from '@/api/ltilaunch.js'
import router from '@/router'

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
            ltiJWT: '',

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
        loadLtiData () {
            return new Promise((resolve, reject) => {
                ltiApi.get_lti_params_from_jwt(this.ltiJWT)
                    .then(response => {
                        this.lti.ltiCourseName = response.lti_cName
                        this.lti.ltiCourseAbbr = response.lti_abbr
                        this.lti.ltiCourseID = response.lti_cID
                        this.lti.ltiAssignName = response.lti_aName
                        this.lti.ltiAssignID = response.lti_aID
                        this.lti.ltiPointsPossible = response.lti_points_possible
                        this.page.cID = response.cID
                        this.page.aID = response.aID
                        this.page.jID = response.jID
                        this.states.state = response.state
                        resolve('success')
                    })
                    .catch(_ => reject(new Error('Error while loading LTI information')))
            })
        },
        handleActions (args) {
            switch (args[0]) {
            case 'courseCreated':
                this.handleCourseChoice = false
                this.page.cID = args[1]
                this.$toasted.success('Course Created!')
                this.states.state = this.states.create_assign
                break
            case 'courseConnected':
                this.handleCourseChoice = false
                this.page.cID = args[1]
                this.$toasted.success('Course Connected!')
                this.states.state = this.states.check_assign
                break
            case 'assignmentIntegrated':
                this.handleAssignmentChoice = false
                this.$toasted.success('Assignment Integrated!')
                this.states.state = this.states.finish_t
                break
            case 'assignmentCreated':
                this.createAssignment = false
                this.page.aID = args[1]
                this.$toasted.success('Assignment Created!')
                this.states.state = this.states.finish_t
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
            case this.states.finish_s:
                this.$router.push({
                    name: 'Journal',
                    params: {
                        cID: this.page.cID,
                        aID: this.page.aID,
                        jID: this.page.jID
                    }
                })
                break
            case this.states.finish_t:
                this.$router.push({
                    name: 'Assignment',
                    params: {
                        cID: this.page.cID,
                        aID: this.page.aID
                    }
                })
                break
            }
        }
    },
    watch: {
        'states.state': function (val) {
            this.updateState(this.states.state)
        }
    },
    async mounted () {
        this.ltiJWT = this.$route.query.ltiJWT
        await this.loadLtiData()
            .catch(err => {
                router.push({
                    name: 'ErrorPage',
                    params: {
                        code: '404',
                        message: err,
                        description: `Error while loading LTI information.
                                        Please contact your system administrator
                                        for more information. Further integration
                                        is not possible.`
                    }
                })
            })

        if (this.states.state === this.states.bad_auth) {
            router.push({
                name: 'ErrorPage',
                params: {
                    code: '511',
                    message: 'Network authorization required',
                    description: `Invalid credentials from the LTI environment.
                                  Please contact your system administrator.`
                }
            })
        } else if (this.states.state === this.states.no_course) {
            router.push({
                name: 'ErrorPage',
                params: {
                    code: '404',
                    message: 'No course found with given ID',
                    description: `The requested course is not available on
                                  ejournal. Wait for it to become availible or
                                  contact your teacher for more information.`
                }
            })
        } else if (this.states.state === this.states.no_assign) {
            router.push({
                name: 'ErrorPage',
                params: {
                    code: '404',
                    message: 'No assignment found with given ID',
                    description: `The requested assignment is not available on
                                  ejournal. Wait for it to become availible or
                                  contact your teacher for more information.`
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
