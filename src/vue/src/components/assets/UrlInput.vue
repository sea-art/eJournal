<template>
    <b-input
        v-model="url"
        :placeholder="(placeholder) ? placeholder : 'Please enter a URL...'"
        :state="state"
        class="multi-form theme-input"
        @change="handleUrlInput"
    />
</template>

<script>
import validation from '@/utils/validation.js'

export default {
    props: ['placeholder'],
    data () {
        return {
            url: null,
            state: null,
        }
    },
    created () {
        if (this.placeholder) {
            this.state = validation.validateURL(this.placeholder, false)
        }
    },
    methods: {
        handleUrlInput (input) {
            if (input) {
                if (!validation.validateURL(input, true)) {
                    this.state = false
                } else {
                    this.$emit('correctUrlInput', input)
                    this.state = true
                }
            } else { // Empty input (input deleted)
                this.state = null
            }
        },
    },
}
</script>
