<template>
    <content-columns>
        <h1 slot="main-content-column">Profile Page</h1>
        <img slot="main-content-column" src="../assets/ohno.jpeg">
        <router-link slot="main-content-column" tag="button" :to='"/Home"'>Back</router-link>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'

export default {
    name: 'Profile',
    components: {
        'content-columns': contentColumns
    }
}
</script>
