<template>
    <!-- TODO: Create default formats. -->
    <b-form @submit.prevent="onSubmit" @reset.prevent="onReset">
        <b-input
            class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input"
            v-model="form.assignmentName"
            placeholder="Assignment name"
            required
        />
        <text-editor
            :id="'text-editor-assignment-description'"
            :givenContent="'Description of the assignment'"
            @content-update="form.assignmentDescription = $event"
            :footer="false"
        />
        <b-button class="float-left change-button mt-2" type="reset">
            <icon name="undo"/>
            Reset
        </b-button>
        <b-button class="float-right add-button mt-2" type="submit">
            <icon name="plus-square"/>
            Create
        </b-button>
    </b-form>
</template>

<script>
import textEditor from '@/components/assets/TextEditor.vue'
import icon from 'vue-awesome/components/Icon'

import assignmentAPI from '@/api/assignment'

export default {
    name: 'CreateAssignment',
    props: ['ltiAssignName', 'ltiAssignID', 'ltiPointsPossible'],
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
        'text-editor': textEditor,
        icon
    },
    methods: {
        onSubmit () {
            assignmentAPI.create({
                name: this.form.assignmentName,
                description: this.form.assignmentDescription,
                course_id: this.form.courseID,
                lti_id: this.form.ltiAssignID,
                points_possible: this.form.pointsPossible
            })
                .then(assignment => {
                    this.$emit('handleAction', assignment.id)
                    this.onReset(undefined)
                    this.$store.dispatch('user/populateStore').catch(_ => {
                        this.$toasted.error('The website might be out of sync, please login again.')
                    })
                })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        },
        onReset (evt) {
            if (evt !== undefined) {
                evt.preventDefault()
            }
            /* Reset our form values */
            this.form.assignmentName = ''
            this.form.assignmentDescription = ''

            /* Trick to reset/clear native browser form validation state */
            this.show = false
            this.$nextTick(() => { this.show = true })
        }
    },
    mounted () {
        if (this.ltiAssignName && this.ltiAssignID && this.ltiPointsPossible) {
            this.form.assignmentName = this.ltiAssignName
            this.form.ltiAssignID = this.ltiAssignID
            this.form.pointsPossible = this.ltiPointsPossible
        }

        this.form.courseID = this.$route.params.cID
    }
}
</script>
