<template>
    <b-input v-model="url" :placeholder="(placeholder) ? placeholder : 'Please enter a URL.'" @change="handleUrlInput"></b-input>
</template>

<script>
import validation from '@/utils/validation.js'

export default {
    props: ['placeholder'],
    data () {
        return {
            url: null
        }
    },
    methods: {
        handleUrlInput (input) {
            if (!validation.validateURL(input)) {
                // Set tooltip and redcolor
            } else {
                this.$emit('correctUrlInput', input)
            }
        }
    }
}
</script>

<style lang="sass" scoped>
</style>
