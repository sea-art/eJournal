<template>
    <content-student-column>
        <h1 class="title-container">User Integration</h1>
        <lti-create-connect-user v-if="handleUserIntegration" @handleAction="userIntegrated"/>
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
            }
        }
    },
    methods: {
        userIntegrated (args) {

        },
        updateState (state) {
            switch (state) {
            case this.states.bad_auth:
                this.$router.push({
                    name: 'ErrorPage',
                    params: {
                        errorCode: '511',
                        errorMessage: 'Network authorization required'
                    }
                })
                break
            case this.states.no_user:
                handleUserIntegration = true
                break
            case this.states.logged_in:
                // TODO: Add property with uID en JWT token.
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
            this.updateState(this.states.state)
        }
    },
    mounted () {
        if (this.$route.query.jwt_access !== undefined) {
            localStorage.setItem('jwt_access', this.$route.query.jwt_access)
        }

        if (this.$route.query.jwt_refresh !== undefined) {
            localStorage.setItem('jwt_refresh', this.$route.query.jwt_refresh)
        }

        router.app.validToken = true
        this.states.state = '0'
        this.updateState(this.states.state)
    }
}
</script>
