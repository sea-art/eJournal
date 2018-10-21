<template>
    <b-card class="no-hover">
        <b-form @submit.prevent="onSubmit" @reset.prevent="onReset">
            <pretty-checkbox
                class="p-svg float-right mt-1"
                color="primary"
                id="publishCheckbox"
                @change="updatePublishTooltip"
                v-model="form.isPublished"
                v-b-tooltip.hover="form.isPublished ? 'Visible to students' : 'Invisible to students'"
                toggle>
                <svg slot="extra" class="svg svg-icon" viewBox="0 0 20 20">
                    <path d="M7.629,14.566c0.125,0.125,0.291,0.188,0.456,0.188c0.164,0,0.329-0.062,0.456-0.188l8.219-8.221c0.252-0.252,0.252-0.659,0-0.911c-0.252-0.252-0.659-0.252-0.911,0l-7.764,7.763L4.152,9.267c-0.252-0.251-0.66-0.251-0.911,0c-0.252,0.252-0.252,0.66,0,0.911L7.629,14.566z"
                          style="stroke: white;fill:white">
                    </path>
                </svg>
                    <b>Published</b>
                <label slot="off-label">Unpublished</label>
            </pretty-checkbox>

            <h2 class="field-heading">Assignment Name</h2>
            <b-input class="multi-form theme-input"
                v-model="form.assignmentName"
                placeholder="Assignment name"
                required
            />
            <h2 class="field-heading">Description</h2>
            <text-editor class="multi-form"
                :id="'text-editor-assignment-description'"
                :givenContent="'Description of the assignment'"
                @content-update="form.assignmentDescription = $event"
                :footer="false"
            />
            <h2 class="field-heading">Points possible</h2>
            <b-input class="multi-form theme-input"
            v-model="form.pointsPossible"
            placeholder="Points"
            type="number"/>
            <b-row>
                <b-col xl="4">
                    <h2 class="field-heading">Unlock date</h2>
                    <flat-pickr class="multi-form theme-input full-width"
                    v-model="form.unlockDate"
                    :config="$root.flatPickrTimeConfig"/>
                </b-col>
                <b-col xl="4">
                    <h2 class="field-heading">Due date</h2>
                    <flat-pickr class="multi-form theme-input full-width"
                    v-model="form.dueDate"
                    :config="$root.flatPickrTimeConfig"/>
                </b-col>
                <b-col xl="4">
                    <h2 class="field-heading">Lock date</h2>
                    <flat-pickr class="multi-form theme-input full-width"
                    v-model="form.lockDate"
                    :config="$root.flatPickrTimeConfig"/>
                </b-col>
            </b-row>
            <b-button class="float-left change-button mt-2" type="reset">
                <icon name="undo"/>
                Reset
            </b-button>
            <b-button class="float-right add-button mt-2" type="submit">
                <icon name="plus-square"/>
                Create
            </b-button>
        </b-form>
    </b-card>
</template>

<script>
import textEditor from '@/components/assets/TextEditor.vue'
import icon from 'vue-awesome/components/Icon'

import assignmentAPI from '@/api/assignment'

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
                pointsPossible: null,
                unlockDate: null,
                dueDate: null,
                lockDate: null,
                isPublished: false
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
                points_possible: this.form.pointsPossible,
                unlock_date: this.form.unlockDate,
                due_date: this.form.dueDate,
                lock_date: this.form.lockDate,
                is_published: this.form.isPublished
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
            this.form.unlockDate = undefined
            this.form.dueDate = undefined
            this.form.lockDate = undefined
            this.form.isPublished = false

            /* Trick to reset/clear native browser form validation state */
            this.show = false
            this.$nextTick(() => { this.show = true })
        },
        updatePublishTooltip () {
            /* Ensures correct value of is_publish is set through v-model and the title bind can update.
             * Still has issues with fast cursor movement triggering focus inbetween. */
            this.$nextTick(() => {
                this.$root.$emit('bv::hide::tooltip', 'publishCheckboxTooltip')
                this.$root.$emit('bv::show::tooltip', 'publishCheckboxTooltip')
            })
        }
    },
    mounted () {
        if (this.lti !== undefined) {
            this.form.assignmentName = this.lti.ltiAssignName
            this.form.ltiAssignID = this.lti.ltiAssignID
            this.form.pointsPossible = this.lti.ltiPointsPossible
            this.form.unlockDate = this.lti.ltiAssignUnlock.slice(0, -9)
            this.form.dueDate = this.lti.ltiAssignDue.slice(0, -9)
            this.form.lockDate = this.lti.ltiAssignLock.slice(0, -9)
            this.form.courseID = this.page.cID
            this.form.isPublished = this.lti.ltiAssignPublished
        } else {
            this.form.courseID = this.$route.params.cID
        }
    }
}
</script>

<style lang="scss">
$pretty--color-primary: #252C39;
@import 'pretty-checkbox/src/pretty-checkbox.scss';
</style>
