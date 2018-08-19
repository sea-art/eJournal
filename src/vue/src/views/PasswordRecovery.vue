<template>
    <content-single-column>
        <h1>Password Recovery</h1>
        <b-card class="blue-border no-hover">
            <b-form @submit.prevent="recoverPassword()">
                <b-input class="multi-form theme-input" type="password" v-model="password" required placeholder="New password"/>
                <b-input class="multi-form theme-input" type="password" v-model="passwordRepeated" @keyup.enter="handleLogin()" required placeholder="Repeat new password"/>
                <b-button class="float-right multi-form add-button" type="submit">
                    <icon name="save"/>
                    Save
                </b-button>
            </b-form>
        </b-card>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import icon from 'vue-awesome/components/Icon'
import authAPI from '@/api/auth.js'

export default {
    name: 'PasswordRecovery',
    props: ['username', 'recoveryToken'],
    data () {
        return {
            password: '',
            passwordRepeated: ''
        }
    },
    methods: {
        validatePassword () {
            if (this.password !== this.passwordRepeated) {
                this.$toasted.error('Passwords do not match!')
                return false
            }
            if (this.password.length < 8) {
                this.$toasted.error('Password needs to contain at least 8 characters.')
                return false
            }
            if (this.password.toLowerCase() === this.password) {
                this.$toasted.error('Password needs to contain at least 1 capital letter.')
                return false
            }
            let re = /[ !@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/
            if (!re.test(this.password)) {
                this.$toasted.error('Password needs to contain a special character.')
                return false
            }
        },
        recoverPassword () {
            // if (this.validatePassword()) {
            authAPI.recoverPassword(this.username, this.recoveryToken, this.password)
                .then(response => {
                    this.validated = true
                    console.log(response)
                })
                .catch(response => {
                    this.$toasted.error(response.response.data.description)
                    // this.$router.push({name: 'Login'})
                })
            // }
        }
    },
    components: {
        'content-single-column': contentSingleColumn,
        icon
    }
}
</script>

<style lang="sass">
.validating-box
    text-align: center

.validating-box h2
    text-align: center
</style>
