<template>
    <b-card class="no-hover">
        <div v-for="a in assignments" :key="a.id">
            <assignment-card @click.native="linkAssignment(a.id)" :line1="a.name">
                <progress-bar v-if="a.journal && a.journal.stats" :currentPoints="a.journal.stats.acquired_points" :totalPoints="a.journal.stats.total_points"></progress-bar>
            </assignment-card>
        </div>
    </b-card>
</template>

<script>
import assignmentCard from '@/components/assignment/AssignmentCard.vue'
import assignmentAPI from '@/api/assignment'

export default {
    name: 'LinkAssignment',
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
            assignmentAPI.getAllFromCourse(this.page.cID)
                .then(assignments => { this.assignments = assignments })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        },
        linkAssignment (aID) {
            assignmentAPI.update(aID, {lti_id: this.lti.ltiAssignID,
                points_possible: this.lti.ltiPointsPossible,
                unlock_date: this.lti.ltiAssignUnlock,
                due_date: this.lti.ltiAssignDue,
                lock_date: this.lti.ltiAssignLock})
                .then(assignment => { this.$emit('handleAction', assignment.id) })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        }
    },
    created () {
        this.loadAssignments()
    }
}
</script>
