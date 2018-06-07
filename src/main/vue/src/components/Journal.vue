<template>
    <div>
        <h1>{{ msg }}</h1>
        Hello {{ $route.params.student }}
        Hello {{ $route.params.assign }}
        Hello {{ $route.params.course }}
    </div>
</template>

<script>
    export default {
        name : 'journal',
        data () {
            return {
                msg : 'Journal'
            }
        }
    }
</script>
