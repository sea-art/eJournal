<template>
    <b-card :class="$root.getBorderClass($route.params.cID)">
        <div class="d-flex float-right multi-form">
            <b-button v-if="assignmentDetails.is_published" @click="assignmentDetails.is_published = false" class="add-button flex-grow-1" v-b-tooltip.hover title="This assignment is visible to students">
                <icon name="check"/>
                Published
            </b-button>
            <b-button v-if="!assignmentDetails.is_published" @click="assignmentDetails.is_published = true" class="delete-button flex-grow-1" v-b-tooltip.hover title="This assignment is not visible to students">
                <icon name="times"/>
                Unpublished
            </b-button>
        </div>
        <h2 class="multi-form">Assignment details</h2>
        <b-form @submit.prevent="onSubmit">
            <h2 class="field-heading">Assignment name</h2>
            <b-input class="multi-form theme-input"
                     v-model="assignmentDetails.name"
                     placeholder="Assignment name"/>
            <h2 class="field-heading">Description</h2>
            <text-editor class="multi-form"
                :id="'text-editor-assignment-edit-description'"
                placeholder="Enter the description of the assignment here"
                v-model="assignmentDetails.description"
                :footer="false"/>
            <h2 class="field-heading">
                Points possible
                <tooltip tip="The amount of points that represents a perfect score for this assignment, excluding bonus points"/>
            </h2>
            <b-input class="multi-form theme-input"
                v-model="assignmentDetails.points_possible"
                placeholder="Points"
                type="number"/>
            <b-row>
                <b-col xl="4">
                    <h2 class="field-heading">
                        Unlock date
                        <tooltip tip="Students will be able to work on the assignment from this date onwards"/>
                    </h2>
                    <flat-pickr class="multi-form theme-input full-width"
                        v-model="assignmentDetails.unlock_date"
                        :config="unlockDateConfig"/>
                </b-col>
                <b-col xl="4">
                    <h2 class="field-heading">
                        Due date
                        <tooltip tip="Students are expected to have finished their assignment by this date, but new entries can still be added until the lock date"/>
                    </h2>
                    <flat-pickr class="multi-form theme-input full-width"
                        v-model="assignmentDetails.due_date"
                        :config="dueDateConfig"/>
                </b-col>
                <b-col xl="4">
                    <h2 class="field-heading">
                        Lock date
                        <tooltip tip="No more entries can be added after this date" />
                    </h2>
                    <flat-pickr class="multi-form theme-input full-width"
                        v-model="assignmentDetails.lock_date"
                        :config="lockDateConfig"/>
                </b-col>
            </b-row>
        </b-form>
        <b-button
            v-if="$hasPermission('can_delete_assignment')"
            class="delete-button full-width mb-4"
            @click="deleteAssignment">
            <icon name="trash"/>
            {{ this.assignmentDetails.course_count > 1 ? 'Remove' : 'Delete' }} Assignment
        </b-button>
    </b-card>
</template>

<script>
import textEditor from '@/components/assets/TextEditor.vue'
import tooltip from '@/components/assets/Tooltip.vue'
import icon from 'vue-awesome/components/Icon'
import assignmentAPI from '@/api/assignment'

export default {
    name: 'FormatEditAssignmentDetailsCard',
    props: {
        assignmentDetails: {
            required: true
        },
        presetNodes: {
            required: true
        }
    },
    components: {
        textEditor,
        tooltip,
        icon
    },
    data () {
        return {
            prevDate: ''
        }
    },
    computed: {
        unlockDateConfig () {
            var maxDate

            for (var key in this.presetNodes) {
                var node = this.presetNodes[key]

                if (new Date(node.due_date) < new Date(maxDate) || !maxDate) {
                    maxDate = node.due_date
                }

                if (node.type !== 'p') {
                    if (new Date(node.unlock_date) < new Date(maxDate) || !maxDate) {
                        maxDate = node.unlock_date
                    }

                    if (new Date(node.lock_date) < new Date(maxDate) || !maxDate) {
                        maxDate = node.lock_date
                    }
                }
            }

            if (new Date(this.assignmentDetails.due_date) < new Date(maxDate) || !maxDate) {
                maxDate = this.assignmentDetails.due_date
            }

            if (!maxDate) {
                maxDate = this.assignmentDetails.lock_date
            }

            return Object.assign({}, { maxDate: maxDate }, this.$root.flatPickrTimeConfig)
        },
        dueDateConfig () {
            var minDate

            for (var key in this.presetNodes) {
                var node = this.presetNodes[key]

                if (new Date(node.due_date) > new Date(minDate) || !minDate) {
                    minDate = node.due_date
                }
            }

            if (!minDate) {
                minDate = this.assignmentDetails.unlock_date
            }

            return Object.assign({}, {
                minDate: minDate,
                maxDate: this.assignmentDetails.lock_date
            }, this.$root.flatPickrTimeConfig)
        },
        lockDateConfig () {
            var minDate

            for (var key in this.presetNodes) {
                var node = this.presetNodes[key]

                if (new Date(node.due_date) > new Date(minDate) || !minDate) {
                    minDate = node.due_date
                }

                if (node.type !== 'p') {
                    if (new Date(node.unlock_date) > new Date(minDate) || !minDate) {
                        minDate = node.unlock_date
                    }

                    if (new Date(node.lock_date) > new Date(minDate) || !minDate) {
                        minDate = node.lock_date
                    }
                }
            }

            if (new Date(this.assignmentDetails.due_date) > new Date(minDate) || !minDate) {
                minDate = this.assignmentDetails.due_date
            }

            if (!minDate) {
                minDate = this.assignmentDetails.lock_date
            }

            return Object.assign({}, { minDate: minDate }, this.$root.flatPickrTimeConfig)
        }
    },
    watch: {
        assignmentDetails: {
            handler: function (newAssignmentDetails) {
                var patt = new RegExp('T')

                /*  When the date is loaded in from the db this format
                    will be adapted to the flatpickr format,
                    which triggers this watcher.
                    These changes happen in the initial load and when it's
                    saved. This will be ignored as an unsaved change by the
                    following regex if-statement.  */
                if (!patt.test(newAssignmentDetails.lock_date) && !patt.test(this.prevDate)) {
                    this.$emit('changed')
                }

                this.prevDate = newAssignmentDetails.lock_date
            },
            deep: true
        }
    },
    methods: {
        deleteAssignment () {
            if (this.assignmentDetails.course_count > 1
                ? confirm('Are you sure you want to remove this assignment from the course?')
                : confirm('Are you sure you want to delete this assignment?')) {
                assignmentAPI.delete(this.assignmentDetails.id, this.$route.params.cID, { customSuccessToast: this.assignmentDetails.course_count > 1 ? 'Removed assignment' : 'Deleted assignment' })
                    .then(() => this.$router.push({
                        name: 'Course',
                        params: {
                            cID: this.$route.params.cID
                        }
                    }))
            }
        }
    }
}
</script>
