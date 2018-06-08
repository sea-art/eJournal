<template>
    <div>
        <h1>{{ msg }}</h1>
        <img src="../assets/ohno.jpeg">
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

<style>
img{
    width:100%;
    max-width:500px;
}
</style>
