<template>
    <b-form @submit.prevent="handleLogin()" id="login-form">
        <b-input class="multi-form" id="formInputUsername" v-model="username" required placeholder="Username"/>
        <b-input class="multi-form" id="formInputPassword" type="password" @keyup.enter="handleLogin()" v-model="password" required placeholder="Password"/>
        <b-button type="submit">Login</b-button><br/>
        <b-button id="forgot-password-button">Forgot password?</b-button>
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
                    this.$emit('login-succes')
                })
                .catch(_ => alert('Could not login'))
        }
    }
}
</script>

<style>
#forgot-password-button {
    margin-top: 10px;
}

#login-form {
    background-color: var(--theme-light-grey);
}
</style>
