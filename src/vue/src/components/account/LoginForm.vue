<template>
    <b-card class="blue-border no-hover card-last-elem-button">
        <b-form @submit.prevent="handleLogin()">
            <b-input class="multi-form theme-input" v-model="username" required placeholder="Username"/>
            <b-input class="multi-form theme-input" type="password" @keyup.enter="handleLogin()" v-model="password" required placeholder="Password"/>
            <b-button class="multi-form change-button" v-b-modal.forgotPasswordModal>
                Forgot password
                <icon name="question"/>
            </b-button>
            <b-button class="float-right multi-form" type="submit">
                <icon name="sign-in"/>
                Log in
            </b-button>
        </b-form>

    <b-modal
        ref="forgotPasswordModalRef"
        id="forgotPasswordModal"
        size="lg"
        @shown="$refs.usernameEmailInput.focus(); usernameEmail=username"
        title="Please enter your username or password"
        hide-footer>
        <b-form @submit.prevent="handleForgotPassword">
            <b-input
                v-model="usernameEmail"
                required
                placeholder="Please enter your username or email"
                ref="usernameEmailInput"
                class="theme-input multi-form"
            />
            <b-button class="delete-button" @click="$refs.forgotPasswordModalRef.hide()">Cancel</b-button>
            <b-button class="float-right" type="submit">Recover password</b-button>
        </b-form>
    </b-modal>

    </b-card>
</template>

<script>
import authAPI from '@/api/auth'
import icon from 'vue-awesome/components/Icon'

export default {
    name: 'LoginForm',
    data () {
        return {
            usernameEmail: null,
            username: null,
            password: null
        }
    },
    methods: {
        handleForgotPassword () {
            let username = ''
            let emailAdress = ''
            let re = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/

            if (re.test(String(this.usernameEmail).toLowerCase())) {
                emailAdress = this.usernameEmail
            } else {
                username = this.usernameEmail
            }

            authAPI.forgotPassword(username, emailAdress)
                .then(response => {
                    this.$refs.forgotPasswordModalRef.hide()
                    this.$toasted.success(response.data.result)
                })
                .catch(response => {
                    this.$toasted.error('No user known by the given information.')
                })
        },
        handleLogin () {
            authAPI.login(this.username, this.password)
                .then(_ => { this.$emit('handleAction') })
                .catch(_ => { this.$toasted.error('Could not login') })
        }
    },
    mounted () {
        if (this.$root.previousPage && this.$root.previousPage.name === 'PasswordRecovery') {
            this.username = this.$root.previousPage.params.username
        }
    },
    components: {
        'icon': icon
    }
}
</script>
