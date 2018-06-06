<template>
    <div>
        <h1>{{ msg }}</h1>
        Hello {{ $route.params.student }}
        Hello {{ $route.params.assign }}
        Hello {{ $route.params.course }}
        <li><router-link :to='"/"+$route.params.course+"/"+$route.params.assign'>Go back to Assignment</router-link></li>

        <!-- <a @click="$router.go(-1)">back</a> -->
    </div>
</template>

<script>
    export default {
        name : 'journal',
        data () {
            return {
                msg : 'Journal',
            }
        }
    }
</script>
