<template>
    <div>
        <h1>{{ msg }}</h1>
        <!-- $route.params.assign is part of the path used by the router see router/index.js -->
        Hello {{ $route.params.assign }} <br>
        <router-link tag="button" to="/Courses/PAV/Colloquium/Dennis">Dennis Journal</router-link>
    </div>
</template>

<script>
export default {
    name: 'assignment',
    data () {
        return {
            msg: 'Docent student overview'
        }
    }
}
</script>
