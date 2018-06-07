<template>
    <div>
        <h1>{{ msg }}</h1>
        <router-link tag="button" :to='"/Courses"'>Back</router-link>
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
