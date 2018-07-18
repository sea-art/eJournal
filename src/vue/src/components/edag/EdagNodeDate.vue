<!--
    Mini component representing the date for a node in the EDAG.
    Handles its own style depending on a state given by parent.
-->

<template>
    <span v-if="dateText !== ''" class="date-text" :class="dateClass"><u>{{ dateText }}</u></span>
</template>

<script>
export default {
    props: ['date', 'selected'],
    computed: {
        dateText () {
            if (!this.date) {
                return ''
            }

            var year = this.date.substring(0, 4)
            var month = this.date.substring(5, 7)
            var day = this.date.substring(8, 10)
            var time = this.date.substring(11, 16)

            return day + '-' + month + '-' + year + ' ' + time
        },
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
