<!--
    Mini component representing the date for a node in the Timeline.
    Handles its own style depending on a state given by parent.
-->

<template>
    <span v-if="date" class="date-text" :class="dateClass">{{ $root.beautifyDate(date, true, this.deadline)}}</span>
</template>

<script>
export default {
    props: ['date', 'selected', 'deadline'],
    computed: {
        dateClass () {
            return this.deadline ? 'deadline-class' : (this.selected ? 'date-selected' : 'date-unselected')
        }
    }
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'

.deadline-class
    opacity: 1
    color: $theme-blue
    font-weight: bold

.date-selected
    opacity: 1

.date-unselected
    opacity: 0.35

.date-text
    text-align: right
    width: 100%
</style>
