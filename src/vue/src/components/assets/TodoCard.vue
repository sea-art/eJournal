<template>
    <b-card :class="$root.getBorderClass(deadline.cID)">
        <todo-square v-if="deadline.totalNeedsMarking" :num="deadline.totalNeedsMarking" class="float-right" />
        <h6>{{ $root.beautifyDate(deadline.deadline) }}</h6>
        <h5>{{ deadline.name }}</h5>
        {{ deadline.courseAbbr }}
    </b-card>
</template>

<script>
import todoSquare from '@/components/assets/TodoSquare.vue'

export default {
    props: ['deadline'],
    components: {
        'todo-square': todoSquare
    }
}
</script>

<style lang="sass" scoped>
@import "~sass/modules/colors.sass"

h6
    display: inline

p
    text-align: right
    font-size: 20px
    color: $theme-blue
    margin-bottom: 0px
</style>
