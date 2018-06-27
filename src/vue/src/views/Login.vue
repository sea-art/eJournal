<template>
    <content-single-column :extraClasses="'pr-2 pl-2'">
        <h1>Login</h1>
        <b-form @submit.prevent="handleLogin()">
            <b-input class="multi-form" v-model="username" required placeholder="Username"/>
            <b-input class="multi-form" type="password" @keyup.enter="handleLogin()" v-model="password" required placeholder="Password"/>
            <b-button class="add-button" type="submit">Login</b-button>
            <b-button class="float-right">Forgot password?</b-button>
        </b-form>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/ContentSingleColumn.vue'
import loginForm from '@/components/LoginForm.vue'
import auth from '@/api/auth.js'

export default {
    name: 'Login',
    props: ['from'],
    data () {
        return {
            username: '',
            password: ''
        }
    },
    methods: {
        handleLoginSucces () {
            // TODO Proper redirect
            this.$router.go(-1)
        },
        handleLogin () {
            auth.login(this.username, this.password)
                .then(_ => {
                    this.handleLoginSucces()
                })
                .catch(_ => alert('Could not login'))
        }
    },
    created () {
        console.log(this.$router)
    },
    beforeRouteUpdate (to, from, next) {
        conole.log('beforeRouteUpdate')
        console.log(from)
    },
    components: {
        'login-form': loginForm,
        'content-single-column': contentSingleColumn
    }
}
</script>
