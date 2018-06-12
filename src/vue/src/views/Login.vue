<template>
    <div class="login">
        <h1>{{ msg }}</h1>
        Welcome to eDag {{ $route.params.course }} <br>

        <b-container fluid>
            <form v-on:submit.prevent="onSubmit">
                <b-col align-self="center"><input v-model="login" ref="username" placeholder="Username"></b-col>
                <b-col align-self="center"><input v-model="password" ref="password" placeholder="Password" type="password"></b-col>
            </form>
        </b-container>

        <!-- <input v-model="login" placeholder="Username"> -->
        <!-- <input type="password" v-model="password" placeholder="Password"> -->

        <!-- <b-button><b-link :to="'/Dashboard'">Login</b-link></b-button> -->
        <!-- <b-button>Register</b-button> -->

        <button tag="b-button" v-on:click="send_login()">Login</button>
        <router-link tag="b-button" to="/">Register</router-link>
        <button tag="b-button" v-on:click="access_resources()">SUPER HAX0R</button>

    </div>
</template>

<script>
import auth from '@/api/auth'

export default {
    name: 'login',
    data () {
        return {
            login: '',
            password: '',
            msg: 'Login'
        }
    },
    methods: {
        send_login() {
            auth.login(this.$refs.username.value, this.$refs.password.value)
        },
        access_resources() {
            auth.authenticated_get('get_user_courses/')
                .then(response => console.log(response))
                .catch(error => console.error(error))
        }
    }
}
</script>
