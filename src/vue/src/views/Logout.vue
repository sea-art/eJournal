<template>
    <h2>Logging out</h2>
</template>

<script>
import authAPI from '@/api/auth.js'

export default {
    created () {
        this.isGuest = true
        authAPI.logout()
        this.$router.push({name: 'Guest'})
    }
}
</script>
