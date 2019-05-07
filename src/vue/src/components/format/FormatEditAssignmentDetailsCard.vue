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
            class="delete-button full-width mb-4"
            @click="deleteAssignment"
        >
            <icon name="trash"/>
            {{ assignmentDetails.course_count > 1 ? 'Remove' : 'Delete' }} Assignment
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
    data () {
        return {
            prevDate: '',
        }
    },
    watch: {
        assignmentDetails: {
            handler (newAssignmentDetails) {
                const patt = new RegExp('T')

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
            deep: true,
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
