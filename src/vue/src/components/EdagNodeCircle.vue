<!--
    Mini component representing the circle for a node in the EDAG.
    Handles its own style depending on a state given by parent.
-->

<template>
    <div class="d-flex align-items-center justify-content-center text-white" :style="styleObject">
        {{ this.text }}
    </div>
</template>

<script>
export default {
    props: ['type', 'text', 'selected'],
    computed: {
        color () {
            if (this.type === 'entry') {
                if (this.selected) {
                    return 'var(--theme-dark-grey)'
                }
                return 'var(--theme-medium-grey)'
            }
            if (this.type === 'progress') {
                if (this.selected) {
                    return 'var(--theme-red)'
                }
                return 'var(--theme-pink)'
            }
        },
        size () {
            return (this.selected) ? '5em' : '4em'
        },
        styleObject () {
            return {
                backgroundColor: this.color,
                width: this.size,
                height: this.size,
                'border-radius': '50% !important',
                'border-style': 'solid',
                'border-width': '5px',
                'border-color': 'white'
            }
        }
    }
}
</script>

<style>
.text-white {
    color: white;
}
</style>
