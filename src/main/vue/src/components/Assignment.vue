<template>
    <div>
        <li><router-link to="/PAV/Colloquium/Dennis">Journal</router-link></li>
        <h1>{{ msg }}</h1>
        Hello {{ $route.params.assign }}
    </div>
</template>

<script>
    export default {
        name : 'assignment',
        data () {
            return {
                msg : 'Assignment'
            }
        }
    }
</script>
