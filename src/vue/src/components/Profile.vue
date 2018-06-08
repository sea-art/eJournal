<template>
    <div>
        <h1>{{ msg }}</h1>
        <router-link tag="button" :to='"/Dashboard"'>Back</router-link>
    </div>
</template>

<script>
export default {
    name: 'edit',
    data () {
        return {
            msg: 'Profile'
        }
    }
}
</script>
