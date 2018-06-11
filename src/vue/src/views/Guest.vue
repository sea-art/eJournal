<template>
    <div>
        <h1>Login</h1>
        Welcome to eDag {{ $route.params.course }} <br>

        <b-container fluid>
            <b-col align-self="center"><input v-model="login" placeholder="Username"></b-col>
            <b-col align-self="center"><input type="password" v-model="password" placeholder="Password"></b-col>
        </b-container>

        <router-link tag="b-button" to="/Home">Login</router-link>
        <router-link tag="b-button" to="/">Register</router-link>

    </div>
</template>

<script>
export default {
    name: 'Guest',
    data () {
        return {
            login: '',
            password: '',
        }
    }
}
</script>
