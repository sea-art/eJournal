<template>
    <div>
        <span class="multi-form">If you dont have an account on eJournal, you can create an account below. This account will be linked to your
        learning environment from then on.</span>
        <b-row align-h="center">
            <b-button class="lti-button-option multi-form" @click="showModal('createUserRef')">
                <icon name="user-plus" scale="1.8"/>
                <h2 class="lti-button-text">Create account</h2>
            </b-button>
        </b-row>
        <span class="multi-form">If you already have an account on eJournal, and would like to link this account to your
        learning environment. Please press the button below.</span>
        <b-row  align-h="center">
            <b-button class="lti-button-option" @click="showModal('connectUserRef')">
                <icon name="link" scale="1.8"/>
                <h2 class="lti-button-text">Link with existing <br/> eJournal account</h2>
            </b-button>
        </b-row>

        <b-modal
            ref="createUserRef"
            title="Create eJournal account"
            size="lg"
            hide-footer>
                <register-user @handleAction="handleRegistered" :lti="lti"/>
        </b-modal>

        <b-modal
            ref="connectUserRef"
            title="Login to link with your learning environment"
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
