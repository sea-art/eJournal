<!--
    Mini component representing the date for a node in the Timeline.
    Handles its own style depending on a state given by parent.
-->

<template>
    <span v-if="date" class="date-text" :class="dateClass">{{ $root.beautifyDate(date, true, this.isDeadline) }}</span>
</template>

<script>
export default {
    props: ['date', 'selected', 'isDeadline'],
    computed: {
        dateClass () {
            return {
                'deadline-class': this.isDeadline,
                'date-selected': this.selected,
                'date-unselected': !this.selected
            }
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
