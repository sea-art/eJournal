<template>
    <div>
        <h1>{{ msg }}</h1>
        Hello {{ $route.params.course }} <br>
        <router-link tag="button" to="/Courses/PAV/Colloquium">Assignment</router-link>
    </div>
</template>

<script>
    export default {
        name : 'courses',
        data () {
            return {
                msg : 'Courses'
            }
        }
    }
</script>
