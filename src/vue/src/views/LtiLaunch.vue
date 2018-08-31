<template>
    <content-single-columns>
        <h1 class="mb-2">{{ currentPage }}</h1>
        <b-card class="no-hover" :class="this.$root.colors[1]">
            <lti-create-connect-course v-if="handleCourseChoice" @handleAction="handleActions" :lti="lti"/>
            <lti-create-connect-assignment v-else-if="handleAssignmentChoice" @handleAction="handleActions" :lti="lti" :page="page"/>
            <lti-create-assignment v-else-if="createAssignment" @handleAction="handleActions" :lti="lti" :page="page"/>
        </b-card>

    </content-single-columns>
</template>

<script>
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import ltiCreateConnectCourse from '@/components/lti/LtiCreateConnectCourse.vue'
import ltiCreateConnectAssignment from '@/components/lti/LtiCreateConnectAssignment.vue'
import ltiCreateAssignment from '@/components/lti/LtiCreateAssignment.vue'

import assignmentAPI from '@/api/assignment'
import ltiAPI from '@/api/ltilaunch'
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
                ltiCourseStart: '',
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
                ltiAPI.getLtiParams(this.ltiJWT)
                    .then(response => {
                        console.log(response)
                        this.lti.ltiCourseName = response.lti_cName
                        this.lti.ltiCourseAbbr = response.lti_abbr
                        this.lti.ltiCourseID = response.lti_cID
                        this.lti.ltiCourseStart = response.lti_course_start
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
                this.page.aID = args[1]
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
                this.currentPage = 'Assignment Integration'
                this.createAssignment = true
                break
            case this.states.check_assign:
                assignmentAPI.getWithLti(this.lti.ltiAssignID)
                    .then(assignment => {
                        if (assignment === undefined) {
                            this.states.state = this.states.new_assign
                        } else {
                            this.page.aID = assignment.id
                            this.states.state = this.states.finish_t
                        }
                    })
                    .catch(error => {
                        if (error.response.status === 404) {
                            this.states.state = this.states.new_assign
                        } else {
                            this.$toasted.error(error.response.description)
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
                /* Student has created a journal for an existing assignment, we need to update the store. */
                this.$store.dispatch('user/populateStore').then(_ => {
                    this.$router.push({
                        name: 'Journal',
                        params: {
                            cID: this.page.cID,
                            aID: this.page.aID,
                            jID: this.page.jID
                        }
                    })
                }, error => {
                    this.$router.push({
                        name: 'ErrorPage',
                        params: {
                            code: error.response.status,
                            reasonPhrase: error.response.statusText,
                            description: `Unable to acquire the newly created journal data, please try again.`
                        }
                    })
                })
                break
            case this.states.finish_t:
                /* Teacher has created or coupled a new course and or assignment, we need to update the store. */
                this.$store.dispatch('user/populateStore').then(_ => {
                    this.$router.push({
                        name: 'Assignment',
                        params: {
                            cID: this.page.cID,
                            aID: this.page.aID
                        }
                    })
                }, error => {
                    this.$router.push({
                        name: 'ErrorPage',
                        params: {
                            code: error.response.status,
                            reasonPhrase: error.response.statusText,
                            description: `Unable to acquire the newly created assignment data, please try again.`
                        }
                    })
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
            .catch(error => {
                console.log(error)
                this.$router.push({
                    name: 'ErrorPage',
                    params: {
                        code: 400,
                        reasonPhrase: error.response.statusText,
                        description: error.response.data.description
                    }
                })
            })

        if (this.states.state === this.states.bad_auth) {
            router.push({
                name: 'ErrorPage',
                params: {
                    code: '511',
                    reasonPhrase: 'Network authorization required',
                    description: `Invalid credentials from the LTI environment.
                                  Please contact the system administrator.`
                }
            })
        } else if (this.states.state === this.states.no_course) {
            router.push({
                name: 'ErrorPage',
                params: {
                    code: '404',
                    reasonPhrase: 'No course found with given ID',
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
                    reasonPhrase: 'No assignment found with given ID',
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
