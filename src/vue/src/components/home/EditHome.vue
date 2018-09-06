<template>
    <b-form @submit.prevent="onSubmit" @reset.prevent="onReset">
        <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input" type="text" v-model="instituteName" placeholder="Institute name"/>
        <!-- TODO less placeholdery -->
        <b-button class="float-right delete-button" type="reset">
            <icon name="undo"/>
            Reset
        </b-button>
        <b-button class="float-right add-button" type="submit">
            <icon name="save"/>
            Save
        </b-button>
    </b-form>
</template>

<script>
import icon from 'vue-awesome/components/Icon'

export default {
    name: 'EditHome',
    data () {
        return {
            instituteName: ''
        }
    },
    methods: {
        onSubmit (evt) {
            /* TODO: Insert submission API. */
        },
        onReset (evt) {
            evt.preventDefault()
            /* Reset our form values */
            this.instituteName = ''

            /* Trick to reset/clear native browser form validation state */
            this.show = false
            this.$nextTick(() => { this.show = true })
        }
    },
    components: {
        icon
    }
}
</script>
