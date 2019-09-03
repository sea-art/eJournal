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
        <h2 class="multi-form">
            Assignment details
        </h2>
        <b-form @submit.prevent="onSubmit">
            <h2 class="field-heading">
                Assignment name
            </h2>
            <b-input
                v-model="assignmentDetails.name"
                class="multi-form theme-input"
                placeholder="Assignment name"
            />
            <h2 class="field-heading">
                Description
            </h2>
            <text-editor
                :id="'text-editor-assignment-edit-description'"
                v-model="assignmentDetails.description"
                :footer="false"
                class="multi-form"
                placeholder="Enter the description of the assignment here"
            />
            <h2 class="field-heading">
                Points possible
                <tooltip
                    tip="The amount of points that represents a perfect score for this assignment, excluding \
                    bonus points"
                />
            </h2>
            <b-input
                v-model="assignmentDetails.points_possible"
                class="multi-form theme-input"
                placeholder="Points"
                type="number"
            />
            <b-row>
                <b-col xl="4">
                    <h2 class="field-heading">
                        Unlock date
                        <tooltip tip="Students will be able to work on the assignment from this date onwards"/>
                    </h2>
                    <flat-pickr
                        v-model="assignmentDetails.unlock_date"
                        class="multi-form theme-input full-width"
                        :config="unlockDateConfig"
                    />
                </b-col>
                <b-col xl="4">
                    <h2 class="field-heading">
                        Due date
                        <tooltip
                            tip="Students are expected to have finished their assignment by this date, but new \
                            entries can still be added until the lock date"
                        />
                    </h2>
                    <flat-pickr
                        v-model="assignmentDetails.due_date"
                        class="multi-form theme-input full-width"
                        :config="dueDateConfig"
                    />
                </b-col>
                <b-col xl="4">
                    <h2 class="field-heading">
                        Lock date
                        <tooltip tip="No more entries can be added after this date"/>
                    </h2>
                    <flat-pickr
                        v-model="assignmentDetails.lock_date"
                        class="multi-form theme-input full-width"
                        :config="lockDateConfig"
                    />
                </b-col>
            </b-row>
        </b-form>
        <b-button
            v-if="$hasPermission('can_delete_assignment')"
            class="delete-button full-width"
            @click="deleteAssignment"
        >
            <icon name="trash"/>
            {{ assignmentDetails.course_count > 1 ? 'Remove' : 'Delete' }} assignment
        </b-button>
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
        unlockDateConfig () {
            let maxDate

            this.presetNodes.forEach((node) => {
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
            })

            if (new Date(this.assignmentDetails.due_date) < new Date(maxDate) || !maxDate) {
                maxDate = this.assignmentDetails.due_date
            }

            if (!maxDate) {
                maxDate = this.assignmentDetails.lock_date
            }

            return Object.assign({}, { maxDate }, this.$root.flatPickrTimeConfig)
        },
        dueDateConfig () {
            let minDate

            this.presetNodes.forEach((node) => {
                if (new Date(node.due_date) > new Date(minDate) || !minDate) {
                    minDate = node.due_date
                }
            })

            if (!minDate) {
                minDate = this.assignmentDetails.unlock_date
            }

            return Object.assign({}, {
                minDate,
                maxDate: this.assignmentDetails.lock_date,
            }, this.$root.flatPickrTimeConfig)
        },
        lockDateConfig () {
            let minDate

            this.presetNodes.forEach((node) => {
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
            })

            if (new Date(this.assignmentDetails.due_date) > new Date(minDate) || !minDate) {
                minDate = this.assignmentDetails.due_date
            }

            if (!minDate) {
                minDate = this.assignmentDetails.lock_date
            }

            return Object.assign({}, { minDate }, this.$root.flatPickrTimeConfig)
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
