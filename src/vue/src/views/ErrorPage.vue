<template>
    <content-columns>
        <h1 slot="main-content-column">404</h1>
        <img src="/static/oh_no/ohno.jpeg" slot="main-content-column">
        <router-link tag="button" :to='"/"' slot="main-content-column">Back to landing page</router-link>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'

export default {
    name: 'Error',
    components: {
        'content-columns': contentColumns
    }
}
</script>
