<template>
    <content-student-column>
        <lti-create-connect-user v-if="handleUserIntegration" @handleAction="userIntegrated"/>
    </content-student-column>
</template>

<script>
import contentSingleColumn from '@/components/ContentSingleColumn.vue'
import ltiCreateConnectUser from '@/components/LtiCreateConnectUser.vue'

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
            case this.states.no_user:
                break
            case this.states.logged_in:
                break
            }
        }
    },
    watch: {
        state: function (val) {
            if (val === this.states.logged_in) {
                this.$router.push({
                    name: 'Journal',
                    params: {
                        cID: this.page.cID,
                        aID: this.page.aID,
                        jID: this.page.jID
                    }
                })
            } else {
                this.updateState(this.states.state)
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

        router.app.validToken = true
        this.states.state = '0'

        if (this.states.state === this.states.bad_auth) {
            this.$router.push({
                name: 'ErrorPage',
                params: {
                    errorCode: '511',
                    errorMessage: 'Network authorization required'
                }
            })
        } else {
            this.updateState(this.states.state)
        }
    }
}
</script>
