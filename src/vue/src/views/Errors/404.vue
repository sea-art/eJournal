<template>
    <content-single-columns>
        <h1 slot="main-content-column">ERROR: 404</h1>
        <img src="../../assets/ohno.jpeg">
    </content-single-columns>
</template>

<script>
import contentSingleColumn from '@/components/ContentSingleColumn.vue'

export default {
    name: 'Error404',
    components: {
        'content-single-columns': contentSingleColumn
    }
}
</script>
