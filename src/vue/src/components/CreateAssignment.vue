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
    name: 'CreateAssignment',
    props: ['lti', 'page'],
    data () {
        return {
            form: {
                assignmentName: '',
                assignmentDescription: '',
                courseID: '',
                ltiAssignID: null,
                pointsPossible: null
            }
        }
    },
    components: {
        'content-single-columns': ContentSingleColumn
    },
    methods: {
        onSubmit () {
            assignmentApi.create_new_assignment(this.form.assignmentName,
                this.form.assignmentDescription, this.form.courseID,
                this.form.ltiAssignID, this.form.pointsPossible)
                .then(response => { this.$emit('handleAction', response.assignment.aID) })
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
    },
    mounted () {
        alert(this.lti)
        if (this.lti !== undefined) {
            this.form.assignmentName = this.lti.ltiAssignName
            this.form.ltiAssignID = this.lti.ltiAssignID
            this.form.pointsPossible = this.lti.ltiPointsPossible
            this.form.courseID = this.page.cID
        } else {
            this.form.courseID = this.$route.params.cID
        }
    }
}
</script>
