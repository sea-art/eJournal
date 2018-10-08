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
            var classes = this.deadline ? 'deadline-class' : ''
            classes += this.selected ? ' date-selected' : ' date-unselected'
            return classes
        }
    }
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'

.date-unselected
    opacity: 0.35

.deadline-class
    opacity: 1
    color: $theme-blue
    font-weight: bold

.date-selected
    opacity: 1
    color: black

.date-text
    text-align: right
    width: 100%
</style>
