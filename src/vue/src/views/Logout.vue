<template>
    <h2>Logging out</h2>
</template>

<script>
export default {
    created () {
        this.$store.dispatch('user/logout')
        this.$router.push({name: 'Guest'})
    }
}
</script>
