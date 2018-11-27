<template>
    <content-single-column>
        <h1>Login</h1>
        <login-form @handleAction="handleLoginSucces"/>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import loginForm from '@/components/account/LoginForm.vue'

export default {
    name: 'Login',
    data () {
        return {
            username: '',
            password: ''
        }
    },
    methods: {
        handleLoginSucces () {
            if (this.$root.previousPage === null) {
                this.$router.push({name: 'Home'})
            }

            switch (this.$root.previousPage.name) {
                case null:
                case 'PasswordRecovery':
                case 'ErrorPage':
                case 'Login':
                case 'LtiLaunch':
                case 'LtiLogin':
                    this.$router.push({name: 'Home'})
                default:
                    this.$router.push({name: this.$root.previousPage.name, params: this.$root.previousPage.params})
            }
        }
    },
    components: {
        'content-single-column': contentSingleColumn,
        'login-form': loginForm
    }
}
</script>
