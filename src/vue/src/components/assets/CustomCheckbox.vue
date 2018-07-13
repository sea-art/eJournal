<template>
    <input type="checkbox" v-model="checked" @click="checkboxToggle">
</template>

<script>
export default {
    name: 'CustomCheckbox',
    props: {
        role: {
            required: true
        },
        permission: {
            required: true
        },
        receivedState: {
            required: true
        }
    },
    data () {
        return {
            checked: ''
        }
    },
    methods: {
        checkboxToggle () {
            this.checked = !this.checked
            this.$emit('checkbox-toggle', [this.role, this.permission, this.checked])
        }
    },
    created () {
        this.checked = this.receivedState
    }
}
</script>
