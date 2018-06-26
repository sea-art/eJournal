<template>
    <b-form @submit.prevent="handleLogin()" class="login-form">
        <b-input class="multi-form" id="formInputUsername" v-model="username" required placeholder="Username"/>
        <b-input class="multi-form" id="formInputPassword" type="password" @keyup.enter="handleLogin()" v-model="password" required placeholder="Password"/>
        <b-button class="multi-form" type="submit">Login</b-button><br/>
        <b-button>Forgot password?</b-button>
    </b-form>
</template>

<script>
import auth from '@/api/auth'

export default {
    data () {
        return {
            username: '',
            password: ''
        }
    },
    methods: {
        handleLogin () {
            auth.login(this.username, this.password)
                .then(_ => {
                    console.log('Login form handle login success')
                    console.log(this)
                    this.$emit('login-success')
                    console.log('After emit')
                })
                .catch(_ => alert('Could not login'))
        }
    }
}
</script>

<style>
.login-form {
    background-color: var(--theme-light-grey);
}
</style>
