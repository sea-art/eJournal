<template>
    <content-single-column>
        <bread-crumb>&nbsp;</bread-crumb>
        <login-form @handleAction="handleLoginSucces"/>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import loginForm from '@/components/account/LoginForm.vue'
import auth from '@/api/auth.js'

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
            } else {
                this.$router.push({name: this.$root.previousPage.name, params: this.$root.previousPage.params})
            }
        },
        handleLogin () {
            auth.login(this.username, this.password)
                .then(_ => {
                    this.handleLoginSucces()
                })
                .catch(_ => {
                    this.$toasted.error('Could not login')
                })
        }
    },
    components: {
        'content-single-column': contentSingleColumn,
        'bread-crumb': breadCrumb,
        'login-form': loginForm
    }
}
</script>
