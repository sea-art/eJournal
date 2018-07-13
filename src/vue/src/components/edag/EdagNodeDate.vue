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
            // TODO Solve with variables as return theme dark and med gray
            return (this.selected) ? '#BBBBBB' : '#DEDEDE'
        },
        dateText () {
            // prettify date
            if (!this.date) {
                return ''
            }

            return this.date
        },
        styleObject () {
            return {
                color: this.color
            }
        }
    }
}
</script>
