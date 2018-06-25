<template>
    <div>
        <b-form @submit="onSubmit" @reset="onReset" :v-model="form.ltiCourseID">
            <!-- TODO: Laad alle courses in en maak single selectable! -->
            <b-button class="float-right" type="reset">Reset</b-button>
            <b-button class="float-right" type="submit">Create</b-button>
        </b-form>
    </div>
</template>

<script>
import assignApi from '@/api/assignment.js'

export default {
    name: 'ConnectAssignment',
    data () {
        return {
            form: {
                assignName: '',
                assignAbbreviation: '',
                assignStartdate: '',
                ltiAssignID: ''
            }
        }
    },
    methods: {
        loadCourses () {
            // TODO: Laad alle courses die gekoppeld zouden kunnen worden.
        },
        onSubmit () {
            assignApi.connect_assignment_lti(this.form.assignName,
                this.form.assignAbbreviation, this.form.assignStartdate,
                this.form.ltiAssignID)
                .then(_ => { this.$emit('handleAction') })
        },
        onReset (evt) {
            evt.preventDefault()
            /* Reset our form values */
            this.form.assignName = ''
            this.form.assignAbbreviation = ''
            this.form.assignStartdate = ''

            /* Trick to reset/clear native browser form validation state */
            this.show = false
            this.$nextTick(() => { this.show = true })
        }
    }
}
</script>
