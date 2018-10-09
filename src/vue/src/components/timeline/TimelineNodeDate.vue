<!--
    Mini component representing the date for a node in the Timeline.
    Handles its own style depending on a state given by parent.
-->

<template>
    <span v-if="date" class="date-text" :class="dateClass">
        <icon
            name="calendar"
            class="mb-1 mr-1"
            v-b-tooltip.hover
            title="Upcoming deadline"/>
        {{ $root.beautifyDate(date) }}
    </span>
</template>

<script>
import icon from 'vue-awesome/components/Icon'

export default {
    props: ['date', 'selected', 'isDeadline'],
    computed: {
        dateClass () {
            return {
                'date-selected': this.selected,
                'date-unselected': !this.selected,
                'date-deadline': this.checkDeadline()
            }
        }
    },
    components: {
        icon
    },
    methods: {
        checkDeadline () {
            var currentDate = new Date()
            var deadlineDate = new Date(this.date)

            return currentDate <= deadlineDate && this.isDeadline
        }
    }
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'

.date-text
    text-align: right
    width: 100%
    svg
        visibility: hidden

.date-unselected
    opacity: 0.35
    cursor: pointer
.date-selected
    cursor: auto
    opacity: 1

.date-deadline
    font-weight: bold
    svg
        visibility: visible
</style>
