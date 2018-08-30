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
            if (this.$root.previousPage === null || this.$root.previousPage.name === null ||
                this.$root.previousPage.name === 'PasswordRecovery' || this.$root.previousPage.name === 'ErrorPage' ||
                this.$root.previousPage.name === 'Login') {
                this.$router.push({name: 'Home'})
            } else {
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
