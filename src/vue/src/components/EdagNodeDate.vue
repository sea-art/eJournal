<!--
    Mini component representing the date for a node in the EDAG.
    Handles its own style depending on a state given by parent.
-->

<template>
    <span :style="styleObject">{{ dateText }}</span>
</template>

<script>
export default {
    props: ['date', 'selected'],
    computed: {
        color () {
            return (this.selected) ? 'var(--theme-dark-grey)' : 'var(--theme-medium-grey)'
        },
        dateText () {
            // prettify date
            return this.date.toDateString()
        },
        styleObject () {
            return {
                color: this.color
            }
        }
    }
}
</script>

<style>
</style>
