<template>
    <div>
        <p class="lti-intro-text">You came here from canvas with an unknown
            user account. Do you want to create a new user on Logboek,
            or connect to an existing one?</p>
        <b-row align-h="center">
            <b-button class="lti-button-option" @click="showModal('createUserRef')">
                <h2 class="lti-button-text">Create new user</h2>
            </b-button>
        </b-row>
        <b-row  align-h="center">
            <b-button class="lti-button-option" @click="showModal('connectUserRef')">
                <h2 class="lti-button-text">Connect to existing user</h2>
            </b-button>
        </b-row>

        <b-modal
            ref="createUserRef"
            title="Create user"
            size="lg"
            hide-footer>
                <register-user @handleAction="handleRegistered" :lti="lti"/>
        </b-modal>

        <b-modal
            ref="connectUserRef"
            title="Connect user"
            size="lg"
            hide-footer>
                <login-form @handleAction="handleConnected"/>
        </b-modal>
    </div>
</template>

<script>
import registerUser from '@/components/RegisterUser.vue'
import loginForm from '@/components/LoginForm.vue'
import userApi from '@/api/user.js'

export default {
    name: 'LtiCreateConnectUser',
    props: ['lti'],
    components: {
        'register-user': registerUser,
        'login-form': loginForm
    },
    methods: {
        signal (msg) {
            this.$emit('handleAction', msg)
        },
        showModal (ref) {
            this.$refs[ref].show()
        },
        hideModal (ref) {
            this.$refs[ref].hide()
        },
        handleRegistered () {
            this.hideModal('createUserRef')
            this.signal(['userIntegrated'])
        },
        handleConnected () {
            userApi.updateLtiIdToUser(this.lti.ltiJWT)
                .then(response => {
                    this.hideModal('connectUserRef')
                    this.signal(['userIntegrated'])
                })
        }
    }
}
</script>
