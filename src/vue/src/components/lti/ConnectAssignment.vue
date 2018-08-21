<template>
    <div>
        <div v-for="a in assignments" :key="a.aID">
            <assignment-card @click.native="connectAssignment(a.aID)" :line1="a.name">
                <progress-bar v-if="a.journal && a.journal.stats" :currentPoints="a.journal.stats.acquired_points" :totalPoints="a.journal.stats.total_points"></progress-bar>
            </assignment-card>
        </div>
    </div>
</template>

<script>
import assignmentCard from '@/components/assignment/AssignmentCard.vue'
import assignApi from '@/api/assignment.js'

export default {
    name: 'ConnectAssignment',
    props: ['lti', 'page'],
    components: {
        'assignment-card': assignmentCard
    },
    data () {
        return {
            assignments: []
        }
    },
    methods: {
        loadAssignments () {
            assignApi.get_course_assignments(this.page.cID)
                .then(assignments => { this.assignments = assignments })
                .catch(response => { this.$toasted.error(response.data.description) })
        },
        connectAssignment (aID) {
            assignApi.connect_assignment_lti(aID, this.lti.ltiAssignID, this.lti.ltiPointsPossible)
                .then(assignment => { this.$emit('handleAction', assignment.aID) })
                .catch(response => { this.$toasted.error(response.data.description) })
        }
    },
    created () {
        this.loadAssignments()
    }
}
</script>
