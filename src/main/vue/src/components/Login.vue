<template>
    <div class="login">
        <h1>{{ msg }}</h1>
        Welcome to eDag {{ $route.params.course }} <br>

        <b-container fluid>
            <b-col align-self="center"><input v-model="login" placeholder="Username"></b-col>
            <b-col align-self="center"><input type="password" v-model="password" placeholder="Password"></b-col>
        </b-container>

        <!-- <input v-model="login" placeholder="Username"> -->
        <!-- <input type="password" v-model="password" placeholder="Password"> -->

        <b-button><b-link :to="'/Courses'">Login</b-link></b-button>
        <b-button>Register</b-button>

        <router-link to="/Courses">Login</router-link>
        <!-- <router-link tag="button" to="/">Register</router-link> -->
    </div>
</template>

<script>
export default {
    name: 'login',
    data () {
        return {
            login: '',
            password: '',
            msg: 'Login',
        }
    }
}
</script>
