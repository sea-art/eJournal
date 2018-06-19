<template>
    <content-single-columns>
        <h1>Assignment creation</h1>
        <b-form slot="main-content-column" @submit="onSubmit" @reset="onReset">
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.assignmentName" placeholder="Assignment name"/>
            <b-textarea class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.assignmentDescription" rows="7" placeholder="Assignment description"/>
            <b-button type="submit">Submit</b-button>
            <b-button type="reset">Reset</b-button>
        </b-form>
    </content-single-columns>
</template>

<script>
import ContentSingleColumn from '@/components/ContentSingleColumn.vue'
import assignmentApi from '@/api/assignment.js'

export default {
    name: 'AssignmentCreation',
    data () {
        return {
            form: {
                assignmentName: '',
                assignmentDescription: ''
            }
        }
    },
    components: {
        'content-single-columns': ContentSingleColumn
    },
    methods: {
        onSubmit (evt) {
            assignmentApi.create_new_assignment(this.form.assignmentName, this.form.assignmentDescription, this.$route.params.cID)
                .then(response => { console.log(response) })
        },
        onReset (evt) {
            evt.preventDefault()
            /* Reset our form values */
            this.form.assignmentName = ''
            this.form.assignmentDescription = ''
            /* Trick to reset/clear native browser form validation state */
            this.show = false
            this.$nextTick(() => { this.show = true })
        }
    }
}
</script>
