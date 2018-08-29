<template>
    <div>
        <p class="lti-intro-text">You came here from an LTI environment with an unknown
            user account. Do you want to create a new user on Logboek,
            or connect to an existing one?</p>
        <b-row align-h="center">
            <b-button class="lti-button-option" @click="showModal('createUserRef')">
                <icon name="user-plus" scale="1.8"/>
                <h2 class="lti-button-text">Create new user</h2>
            </b-button>
        </b-row>
        <b-row  align-h="center">
            <b-button class="lti-button-option" @click="showModal('connectUserRef')">
                <icon name="link" scale="1.8"/>
                <h2 class="lti-button-text">Connect to existing user</h2>
            </b-button>
        </b-row>

        <b-modal
            ref="createUserRef"
            title="New User"
            size="lg"
            hide-footer>
                <register-user @handleAction="handleRegistered" :lti="lti"/>
        </b-modal>

        <b-modal
            ref="connectUserRef"
            title="Connect User"
            size="lg"
            hide-footer>
                <login-form @handleAction="handleConnected"/>
        </b-modal>
    </div>
</template>

<script>
import registerUser from '@/components/account/RegisterUser.vue'
import loginForm from '@/components/account/LoginForm.vue'

import userAPI from '@/api/user'
import icon from 'vue-awesome/components/Icon'

export default {
    name: 'LtiCreateConnectUser',
    props: ['lti'],
    components: {
        'register-user': registerUser,
        'login-form': loginForm,
        icon
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
            userAPI.update(0, {jwt_params: this.lti.ltiJWT})
                .then(_ => {
                    this.hideModal('connectUserRef')
                    this.signal(['userIntegrated'])
                })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        }
    }
}
</script>
