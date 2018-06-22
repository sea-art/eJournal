<template>
    <!-- TODO: Maak formats! -->
    <div>
        <b-form @submit="onSubmit" @reset="onReset">
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.assignmentName" placeholder="Assignment name"/>
            <b-textarea class="mb-2 mr-sm-2 mb-sm-0 multi-form" v-model="form.assignmentDescription" rows="6" placeholder="Description of the assignment"/>
            <b-button class="float-right" type="reset">Reset</b-button>
            <b-button class="float-right" type="submit">Create</b-button>
        </b-form>
    </div>
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
        onSubmit () {
            assignmentApi.create_new_assignment(this.form.assignmentName, this.form.assignmentDescription, this.$route.params.cID)
                .then(_ => { this.$emit('handleAction') })
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
