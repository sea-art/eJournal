<template>
    <!-- TODO: Create default formats. -->
    <div>
        <b-form @submit.prevent="onSubmit" @reset.prevent="onReset">
            <b-input class="mb-2 mr-sm-2 mb-sm-0 multi-form theme-input" v-model="form.assignmentName" placeholder="Assignment name"/>
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
    </div>
</template>

<script>
import ContentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import textEditor from '@/components/assets/TextEditor.vue'
import assignmentApi from '@/api/assignment.js'
import icon from 'vue-awesome/components/Icon'

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
        'content-single-columns': ContentSingleColumn,
        'text-editor': textEditor,
        'icon': icon
    },
    methods: {
        onSubmit () {
            assignmentApi.create_new_assignment(this.form.assignmentName,
                this.form.assignmentDescription, this.form.courseID,
                this.form.ltiAssignID, this.form.pointsPossible)
                .then(response => {
                    this.$emit('handleAction', response.assignment.aID)
                    this.onReset(undefined)
                })
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
