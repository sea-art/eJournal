<template>
    <b-card
        :class="$root.getBorderClass($route.params.cID)"
        class="no-hover"
    >
        <div class="d-flex float-right multi-form">
            <b-button
                v-if="assignmentDetails.is_published"
                v-b-tooltip.hover
                class="add-button flex-grow-1"
                title="This assignment is visible to students"
                @click="assignmentDetails.is_published = false"
            >
                <icon name="check"/>
                Published
            </b-button>
            <b-button
                v-if="!assignmentDetails.is_published"
                v-b-tooltip.hover
                class="delete-button flex-grow-1"
                title="This assignment is not visible to students"
                @click="assignmentDetails.is_published = true"
            >
                <icon name="times"/>
                Unpublished
            </b-button>
        </div>
        <h2 class="theme-h2 multi-form">
            Assignment details
        </h2>
        <b-form @submit.prevent="onSubmit">
            <h2 class="theme-h2 field-heading">
                Assignment name
            </h2>
            <b-input
                v-model="assignmentDetails.name"
                class="multi-form theme-input"
                placeholder="Assignment name"
            />
            <h2 class="theme-h2 field-heading">
                Description
            </h2>
            <text-editor
                :id="'text-editor-assignment-edit-description'"
                :key="'text-editor-assignment-edit-description'"
                v-model="assignmentDetails.description"
                :footer="false"
                class="multi-form"
                placeholder="Enter the description of the assignment here"
            />
            <h2 class="theme-h2 field-heading">
                Points possible
                <tooltip
                    tip="The amount of points that represents a perfect score for this assignment, excluding
                    bonus points"
                />
            </h2>
            <b-input
                v-model="assignmentDetails.points_possible"
                class="multi-form theme-input"
                placeholder="Points"
                type="number"
            />
            <h2 class="theme-h2 field-heading">
                Assign to
                <tooltip
                    tip="Assign the assignment only to specific course groups"
                />
            </h2>
            <theme-select
                v-model="assignmentDetails.assigned_groups"
                label="name"
                trackBy="id"
                :options="assignmentDetails.all_groups !== undefined ? assignmentDetails.all_groups : []"
                :multiple="true"
                :searchable="true"
                :multiSelectText="`assigned to group${assignmentDetails.assigned_groups &&
                    assignmentDetails.assigned_groups.length === 1 ? '' : 's'}`"
                placeholder="Everyone"
                class="multi-form mr-2"
            />
            <b-row>
                <b-col xl="4">
                    <h2 class="theme-h2 field-heading">
                        Unlock date
                        <tooltip tip="Students will be able to work on the assignment from this date onwards"/>
                    </h2>
                    <flat-pickr
                        v-model="assignmentDetails.unlock_date"
                        class="multi-form full-width"
                        :config="unlockDateConfig"
                    />
                </b-col>
                <b-col xl="4">
                    <h2 class="theme-h2 field-heading">
                        Due date
                        <tooltip
                            tip="Students are expected to have finished their assignment by this date, but new
                                  entries can still be added until the lock date"
                        />
                    </h2>
                    <flat-pickr
                        v-model="assignmentDetails.due_date"
                        class="multi-form full-width"
                        :config="dueDateConfig"
                    />
                </b-col>
                <b-col xl="4">
                    <h2 class="theme-h2 field-heading">
                        Lock date
                        <tooltip tip="No more entries can be added after this date"/>
                    </h2>
                    <flat-pickr
                        v-model="assignmentDetails.lock_date"
                        class="multi-form full-width"
                        :config="lockDateConfig"
                    />
                </b-col>
            </b-row>
        </b-form>
        <div class="d-flex flex-wrap">
            <b-button
                v-if="$hasPermission('can_delete_assignment')"
                :class="{'input-disabled': assignmentDetails.lti_count > 1 && assignmentDetails.active_lti_course
                    && parseInt(assignmentDetails.active_lti_course.cID) === parseInt($route.params.cID)}"
                class="delete-button multi-form"
                @click="deleteAssignment"
            >
                <icon name="trash"/>
                {{ assignmentDetails.course_count > 1 ? 'Remove' : 'Delete' }} assignment
            </b-button>
        </div>
    </b-card>
</template>

<script>
import textEditor from '@/components/assets/TextEditor.vue'
import tooltip from '@/components/assets/Tooltip.vue'
import assignmentAPI from '@/api/assignment.js'

export default {
    name: 'FormatEditAssignmentDetailsCard',
    components: {
        textEditor,
        tooltip,
    },
    props: {
        assignmentDetails: {
            required: true,
        },
        presetNodes: {
            required: true,
        },
    },
    computed: {
        // Ensure the unlock date cannot be later than any preset date or the assignment due or lock date.
        unlockDateConfig () {
            const additionalConfig = {}

            this.presetNodes.forEach((node) => {
                if (node.unlock_date && (!additionalConfig.maxDate
                    || new Date(node.unlock_date) < additionalConfig.maxDate)) {
                    // Preset has unlock date earlier than current max.
                    additionalConfig.maxDate = new Date(node.unlock_date)
                } else if (node.due_date && (!additionalConfig.maxDate
                    || new Date(node.due_date) < additionalConfig.maxDate)) {
                    // Preset has due date earlier than current max.
                    additionalConfig.maxDate = new Date(node.due_date)
                } else if (node.lock_date && (!additionalConfig.maxDate
                    || new Date(node.lock_date) < additionalConfig.maxDate)) {
                    // Preset has lock date earlier than current max.
                    additionalConfig.maxDate = node.lock_date
                }
            })

            if (this.assignmentDetails.due_date && (!additionalConfig.maxDate
                || new Date(this.assignmentDetails.due_date) < additionalConfig.maxDate)) {
                // Assignment has due date earlier than current max.
                additionalConfig.maxDate = new Date(this.assignmentDetails.due_date)
            } else if (this.assignmentDetails.lock_date && (!additionalConfig.maxDate
                || new Date(this.assignmentDetails.lock_date) < additionalConfig.maxDate)) {
                // Assignment has lock date earlier than current max.
                additionalConfig.maxDate = new Date(this.assignmentDetails.lock_date)
            }

            return Object.assign({}, additionalConfig, this.$root.flatPickrTimeConfig)
        },
        // Ensure the due date cannot be earlier than any preset date or the assignment unlock date, and no later than
        // the assignnment lock date.
        dueDateConfig () {
            const additionalConfig = {}

            this.presetNodes.forEach((node) => {
                if (node.due_date && (!additionalConfig.minDate
                    || new Date(node.due_date) > additionalConfig.minDate)) {
                    // Preset has due date later than current min.
                    additionalConfig.minDate = new Date(node.due_date)
                }
            })

            if (this.assignmentDetails.unlock_date && (!additionalConfig.minDate
                || new Date(this.assignmentDetails.unlock_date) > additionalConfig.minDate)) {
                // Assignment has unlock date later than current min.
                additionalConfig.minDate = new Date(this.assignmentDetails.unlock_date)
            }

            if (this.assignmentDetails.lock_date) {
                // Assignment has lock date, due date cannot be later.
                additionalConfig.maxDate = new Date(this.assignmentDetails.lock_date)
            }

            return Object.assign({}, additionalConfig, this.$root.flatPickrTimeConfig)
        },
        // Ensure the lock date cannot be earlier than any preset date or the assignment due or unlock date.
        lockDateConfig () {
            const additionalConfig = {}

            this.presetNodes.forEach((node) => {
                if (node.unlock_date && (!additionalConfig.minDate
                    || new Date(node.unlock_date) > additionalConfig.minDate)) {
                    // Preset has unlock date later than current min.
                    additionalConfig.minDate = new Date(node.unlock_date)
                } else if (node.due_date && (!additionalConfig.maxDate
                    || new Date(node.due_date) > additionalConfig.maxDate)) {
                    // Preset has due date later than current min.
                    additionalConfig.minDate = new Date(node.due_date)
                } else if (node.lock_date && (!additionalConfig.minDate
                    || new Date(node.lock_date) > additionalConfig.minDate)) {
                    // Preset has lock date later than current min.
                    additionalConfig.minDate = node.lock_date
                }
            })

            if (this.assignmentDetails.due_date && (!additionalConfig.minDate
                || new Date(this.assignmentDetails.due_date) > additionalConfig.minDate)) {
                // Assignment has due date later than current min.
                additionalConfig.minDate = new Date(this.assignmentDetails.due_date)
            } else if (this.assignmentDetails.unlock_date && (!additionalConfig.minDate
                || new Date(this.assignmentDetails.unlock_date) > additionalConfig.minDate)) {
                // Assignment has unlock date later than current min.
                additionalConfig.minDate = new Date(this.assignmentDetails.unlock_date)
            }

            return Object.assign({}, additionalConfig, this.$root.flatPickrTimeConfig)
        },
    },
    methods: {
        deleteAssignment () {
            if (this.assignmentDetails.course_count > 1
                ? window.confirm('Are you sure you want to remove this assignment from the course?')
                : window.confirm('Are you sure you want to delete this assignment?')) {
                assignmentAPI.delete(
                    this.assignmentDetails.id,
                    this.$route.params.cID,
                    {
                        customSuccessToast: this.assignmentDetails.course_count > 1
                            ? 'Removed assignment' : 'Deleted assignment',
                    },
                )
                    .then(() => this.$router.push({
                        name: 'Course',
                        params: {
                            cID: this.$route.params.cID,
                        },
                    }))
            }
        },
    },
}
</script>
