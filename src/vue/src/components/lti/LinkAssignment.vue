<template>
    <b-card class="no-hover">
        <div v-for="a in assignments" :key="a.id">
            <div v-if="a.lti_id">
                <assignment-card class="orange-border" @click.native="linkAssignment(a.id, a.lti_id)" :line1="a.name">
                    <progress-bar v-if="a.journal && a.journal.stats"
                        :currentPoints="a.journal.stats.acquired_points"
                        :totalPoints="a.journal.stats.total_points"/>
                </assignment-card>
            </div>
            <div v-else>
                <assignment-card class="green-border" @click.native="linkAssignment(a.id, a.lti_id)" :line1="a.name">
                    <progress-bar v-if="a.journal && a.journal.stats"
                        :currentPoints="a.journal.stats.acquired_points"
                        :totalPoints="a.journal.stats.total_points"/>
                </assignment-card>
            </div>
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
            if (!aLTI || confirm('This assignment is already linked to another course, are you sure you also want to link it?')) {

            }
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
