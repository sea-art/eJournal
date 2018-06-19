<template>
    <b-form @submit="onSubmit" @reset="onReset">
        <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" type="text" v-model="institueName" placeholder="Institute name"/>
        <b-button class="float-right" type="reset">Reset</b-button>
        <b-button class="float-right" type="submit">Submit</b-button>
    </b-form>
</template>

<script>
export default {
    name: 'EditHome',
    data () {
        return {
            form: {
                institueName: ''
            }
        }
    },
    methods: {
        onSubmit (evt) {
            /* TODO: Insert submission API. */
        },
        onReset (evt) {
            evt.preventDefault()
            /* Reset our form values */
            this.institueName = ''

            /* Trick to reset/clear native browser form validation state */
            this.show = false
            this.$nextTick(() => { this.show = true })
        }
    }
}
</script>
