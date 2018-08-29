<template>
    <div>
        <p class="lti-intro-text">Welcome to eJournal! Would you like to couple with a previously registered account or
            would you like us to create an account for you?</p>
        <b-row align-h="center">
            <b-button class="lti-button-option" @click="showModal('createUserRef')">
                <icon name="user-plus" scale="1.8"/>
                <h2 class="lti-button-text">Create account</h2>
            </b-button>
        </b-row>
        <b-row  align-h="center">
            <b-button class="lti-button-option" @click="showModal('connectUserRef')">
                <icon name="link" scale="1.8"/>
                <h2 class="lti-button-text">Couple account</h2>
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
import userApi from '@/api/user.js'
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
            userApi.updateLtiIdToUser(this.lti.ltiJWT).then(_ => {
                // This is required because between the login and the connect of lti user to our user data can change.
                this.$store.dispatch('user/populateStore').then(_ => {
                    this.hideModal('connectUserRef')
                    this.signal(['userIntegrated'])
                })
            }).catch(error => { this.$toasted.error(error.response.data.description) })
        }
    }
}
</script>
