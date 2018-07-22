<!--
    Mini component representing the date for a node in the EDAG.
    Handles its own style depending on a state given by parent.
-->

<template>
    <span v-if="date !== ''" class="date-text" :class="dateClass"><u>{{ $root.beautifyDate(date) }}</u></span>
</template>

<script>
export default {
    props: ['date', 'selected'],
    computed: {
        dateClass () {
            return (this.selected) ? 'date-selected' : 'date-unselected'
        }
    }
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'

.date-selected
    opacity: 1

.date-unselected
    opacity: 0.5

.date-text
    text-align: right
</style>
