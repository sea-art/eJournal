<template>
    <content-single-column>
        <h1>Login</h1>
        <b-card class="blue-border no-hover card-last-elem-button">
            <b-form @submit.prevent="handleLogin()">
                <b-input class="multi-form" v-model="username" required placeholder="Username"/>
                <b-input class="multi-form" type="password" @keyup.enter="handleLogin()" v-model="password" required placeholder="Password"/>
                <b-button class="add-button" type="submit">Login</b-button>
                <b-button class="float-right">Forgot password?</b-button>
            </b-form>
        </b-card>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/ContentSingleColumn.vue'
import loginForm from '@/components/LoginForm.vue'
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
        'login-form': loginForm,
        'content-single-column': contentSingleColumn
    }
}
</script>
