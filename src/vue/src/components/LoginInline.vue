<template>
    <b-form inline id="inline-login-form">
          <label class="sr-only" for="inlineFormInputUsername">Username</label>
          <b-input class="mb-2 mr-sm-2 mb-sm-0" id="inlineFormInputUsername" v-model="username" placeholder="Username"/>

          <label class="sr-only" for="inlineFormInputPassword">Password</label>
          <b-input class="mb-2 mr-sm-2 mb-sm-0" id="inlineFormInputPassword" v-model="password" placeholder="Password" />

         <b-button class="mb-2 mr-sm-2 mb-sm-0" @click="handleLogin()">Login</b-button>
         <b-button class="mb-2 mr-sm-2 mb-sm-0" @click="handleRegister()">Register</b-button>
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
                .then(this.$router.push('/Home'))
        },
        handleRegister () {
            console.log(this.username)
            console.log(this.password)
        }
    }
}
</script>
