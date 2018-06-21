<template>
    <content-single-columns>
        <h1 slot="main-content-column">Placeholder for the Guest page (Landing page)</h1>
    </content-single-columns>
</template>

<script>
import contentSingleColumn from '@/components/ContentSingleColumn.vue'

export default {
    name: 'Guest',
    components: {
        'content-single-columns': contentSingleColumn
    }
}
</script>
