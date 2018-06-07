<template>
    <div>
        <h1>{{ msg }}</h1>
        Welcome to eDag {{ $route.params.course }} <br>
        <router-link tag="button" to="/Courses">Login</router-link>
        <router-link tag="button" to="/">Register</router-link>
    </div>
</template>

<script>
    export default {
        name : 'login',
        data () {
            return {
                msg : 'Login'
            }
        }
    }
</script>
