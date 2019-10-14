<template>
    <b-card
        :class="$root.getBorderClass($route.params.cID)"
        class="no-hover"
    >
        <assignment-details
            :assignmentDetails="assignmentDetails"
            :presetNodes="presetNodes"
        />
        <b-button
            v-if="$hasPermission('can_delete_assignment')"
            :class="{'input-disabled': assignmentDetails.lti_count > 1 && assignmentDetails.active_lti_course
                && parseInt(assignmentDetails.active_lti_course.cID) === parseInt($route.params.cID)}"
            class="delete-button multi-form mr-md-2 flex-grow-1"
            @click="deleteAssignment"
        >
            <icon name="trash"/>
            {{ assignmentDetails.course_count > 1 ? 'Remove' : 'Delete' }} assignment
        </b-button>
        <b-button
            class="add-button multi-form flex-grow-1"
            @click="$emit('copyFormat')"
        >
            <icon name="file"/>
            Copy other assignment
        </b-button>
    </b-card>
</template>

<script>
import AssignmentDetails from '@/components/assignment/AssignmentDetails.vue'

import assignmentAPI from '@/api/assignment.js'

export default {
    name: 'FormatEditAssignmentDetailsCard',
    components: {
        AssignmentDetails,
    },
    props: {
        presetNodes: {
            required: true,
        },
        assignmentDetails: {
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
                    if ((node.unlock_date && new Date(node.unlock_date) < new Date(maxDate))
                        || !maxDate) {
                        maxDate = node.unlock_date
                    }

                    if ((node.lock_date && new Date(node.lock_date) < new Date(maxDate))
                        || !maxDate) {
                        maxDate = node.lock_date
                    }
                }
            })

            if ((this.assignmentDetails.due_date && new Date(this.assignmentDetails.due_date) < new Date(maxDate))
                || !maxDate) {
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
