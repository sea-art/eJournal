<template>
    <b-input
        class="multi-form theme-input"
        v-model="url"
        :placeholder="(placeholder) ? placeholder : 'Please enter a URL...'"
        @change="handleUrlInput"
        :state="state">
    </b-input>
</template>

<script>
import validation from '@/utils/validation.js'

export default {
    props: ['placeholder'],
    data () {
        return {
            url: null,
            state: null
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
        }
    },
    created () {
        if (this.placeholder) {
            this.state = validation.validateURL(this.placeholder, false)
        }
    }
}
</script>
