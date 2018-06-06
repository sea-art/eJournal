<template>
    <div>
        <li><router-link to="/PAV/Colloquium">Assignment</router-link></li>
        <h1>{{ msg }}</h1>
        Hello {{ $route.params.course }}
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
