<template>
    <b-card class="no-hover" :class="$root.getBorderClass($route.params.cID)">
        <div class="multi-form"><b>Needs marking</b><todo-square class="float-right" :num="stats.needsMarking"/></div>
        <div class="multi-form"><b>Unpublished grades</b><todo-square class="float-right" :num="stats.unpublished"/></div>
        <div><b>Average points</b><todo-square class="float-right" :num="stats.averagePoints"/></div>
    </b-card>
</template>

<script>
import todoSquare from '@/components/assets/TodoSquare.vue'

export default {
    props: ['stats'],
    components: {
        'todo-square': todoSquare
    }
}
</script>
