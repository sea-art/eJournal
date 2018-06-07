<template>
    <div>
        <h1>{{ msg }}</h1>
        Deadline 1
        Deadline 2
        Deadline 3
        <!-- Welcome to eDag {{ $route.params.course }} <br> -->
        <!-- <router-link tag="button" to="/Courses">Login</router-link> -->
        <!-- <router-link tag="button" to="/">Register</router-link> -->
    </div>
</template>

<script>
    export default {
        name : 'deadline',
        data () {
            return {
                msg : 'Deadlines'
            }
        }
    }
</script>
