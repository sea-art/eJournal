<template>
    <b-card
        :class="$root.getBorderClass($route.params.cID)"
        class="no-hover"
    >
        <div class="multi-form">
            <b>Needs marking</b><todo-square
                :num="stats.needsMarking"
                class="float-right"
            />
        </div>
        <div class="multi-form">
            <b>Unpublished grades</b><todo-square
                :num="stats.unpublished"
                class="float-right"
            />
        </div>
        <div>
            <b>Average points</b><todo-square
                :num="stats.averagePoints"
                class="float-right"
            />
        </div>
    </b-card>
</template>

<script>
import todoSquare from '@/components/assets/TodoSquare.vue'

export default {
    components: {
        todoSquare,
    },
    props: ['stats'],
}
</script>
