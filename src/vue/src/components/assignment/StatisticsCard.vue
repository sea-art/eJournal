<template>
    <b-card
        :class="$root.getBorderClass($route.params.cID)"
        class="no-hover"
    >
        <div class="multi-form">
            <b>Needs marking</b><number-badge
                :leftNum="stats.needsMarking"
                class="float-right"
            />
        </div>
        <div class="multi-form">
            <b>Unpublished grades</b><number-badge
                :leftNum="stats.unpublished"
                class="float-right"
            />
        </div>
        <div>
            <b>Average points</b><number-badge
                :leftNum="stats.averagePoints"
                class="float-right"
            />
        </div>
    </b-card>
</template>

<script>
import numberBadge from '@/components/assets/NumberBadge.vue'

export default {
    components: {
        numberBadge,
    },
    props: ['stats'],
}
</script>
