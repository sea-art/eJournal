<template>
    <content-student-column>
        <h1 class="title-container">User Integration</h1>
        <lti-create-connect-user v-if="handleUserIntegration" @handleAction="userIntegrated" :lti="lti"/>
    </content-student-column>
</template>

<script>
import contentSingleColumn from '@/components/ContentSingleColumn.vue'
import ltiCreateConnectUser from '@/components/LtiCreateConnectUser.vue'
import router from '@/router'

export default {
    name: 'LtiLogin',
    components: {
        'content-student-column': contentSingleColumn,
        'lti-create-connect-user': ltiCreateConnectUser
    },
    data () {
        return {
            /* Variables for loading the right component. */
            handleUserIntegration: false,

            /* Possible states for the control flow */
            states: {
                state: '',
                bad_auth: '-1',
                no_user: '0',
                logged_in: '1'
            },

            lti: {
                ltiJWT: '',
                firstname: '',
                lastname: '',
                username: '',
                emaik: ''
            }
        }
    },
    methods: {
        userIntegrated (args) {

        }
    },
    watch: {
        state: function (val) {
            this.updateState(this.states.state)
        }
    },
    mounted () {
        if (this.$route.query.state === this.states.bad_auth) {
            this.$router.push({
                name: 'ErrorPage',
                params: {
                    errorCode: '511',
                    errorMessage: 'Network authorization required'
                }
            })
        } else {
            this.lti.ltiJWT = this.$route.query.lti_params

            if (this.$route.query.state === this.states.logged_in) {
                if (this.$route.query.jwt_access !== undefined) {
                    localStorage.setItem('jwt_access', this.$route.query.jwt_access)
                }

                if (this.$route.query.jwt_refresh !== undefined) {
                    localStorage.setItem('jwt_refresh', this.$route.query.jwt_refresh)
                }

                router.app.validToken = true
            } else if (this.$route.query.state === this.states.no_user) {
                if (this.$route.query.firstname !== undefined) {
                    this.lti.firstname = this.$route.query.firstname
                }
                if (this.$route.query.lastname !== undefined) {
                    this.lti.lastname = this.$route.query.lastname
                }
                if (this.$route.query.username !== undefined) {
                    this.lti.username = this.$route.query.username
                }
                if (this.$route.query.email !== undefined) {
                    this.lti.email = this.$route.query.email
                }

                handleUserIntegration = true
            } else {
                this.$router.push({
                    name: 'ErrorPage',
                    params: {
                        errorCode: '400',
                        errorMessage: 'Bad request'
                    }
                })
            }
        }
    }
}
</script>
