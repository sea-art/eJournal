<template>
    <div class="login">
        <div class="row">
            <div class="col" style="background-color:powderblue;">
                HALLOOO
            </div>
            <div class="col-6">
                <h1>{{ msg }}</h1>
                Welcome to eDag {{ $route.params.course }} <br>

                <input v-model="login" placeholder="Username">
                <input type="password" v-model="password" placeholder="Password">

                <router-link tag="button" to="/Courses">Login</router-link>
                <router-link tag="button" to="/">Register</router-link>
            </div>
            <div class="col" style="background-color:powderblue;">
                HAAAIII
            </div>
        </div>
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
