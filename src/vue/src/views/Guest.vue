<template>
    <content-columns>
        <h1 slot="main-content-column">Placeholder for the Guest page (Landing page)</h1>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'

export default {
    name: 'Guest',
    components: {
        'content-columns': contentColumns
    }
}
</script>
