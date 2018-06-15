<template>
    <content-columns>
        <h1 slot="main-content-column">AssignmentsOverview Page</h1>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'

export default {
    name: 'AssignmentsOverview',
    components: {
        'content-columns': contentColumns
    }
}
</script>
