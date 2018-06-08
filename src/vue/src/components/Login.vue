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

        <!-- <b-button><b-link :to="'/Courses'">Login</b-link></b-button> -->
        <!-- <b-button>Register</b-button> -->

        <router-link tag="b-button" to="/Courses">Login</router-link>
        <router-link tag="b-button" to="/">Register</router-link>

        <b-container class="bv-example-row">
            <b-row class="text-center">
                <b-col class="p-3 mb-2 bg-primary text-white" cols="3">1 of 3</b-col>
                <b-col class="p-3 mb-2 bg-danger text-white" cols="6">2 of 3 (wider)</b-col>
                <b-col class="p-3 mb-2 bg-primary text-white" cols="3">3 of 3</b-col>
            </b-row>
        </b-container>

    </div>
</template>

<script>
export default {
    name: 'login',
    data () {
        return {
            login: '',
            password: '',
            msg: 'Login'
        }
    }
}
</script>
