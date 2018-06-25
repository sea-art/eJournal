<template>
    <div>
        <div v-for="a in assignments" :key="a.aID">
            <assignment-card @click.native="connectAssignment(a.aID)" :line1="a.name" :color="$root.colors[a.aID % $root.colors.length]">
                <progress-bar v-if="a.journal && a.journal.stats" :currentPoints="a.journal.stats.acquired_points" :totalPoints="a.journal.stats.total_points"></progress-bar>
            </assignment-card>
        </div>
    </div>
</template>

<script>
import mainCard from '@/components/MainCard.vue'
import assignApi from '@/api/assignment.js'

export default {
    name: 'ConnectAssignment',
    props: ['lti', 'page'],
    components: {
        'main-card': mainCard
    },
    data () {
        return {
            assignments: []
        }
    },
    methods: {
        loadAssignments () {
            assignApi.get_course_assignments(this.page.cID)
                .then(response => { this.assignments = response })
                .catch(_ => alert('Error while loading assignments'))
        },
        connectAssignment (aID) {
            courseApi.connect_assignment_lti(aID, this.lti.ltiAssignID, this.lti.pointsPossible)
                .then(response => { this.$emit('handleAction', response.aID) })
        }
    },
    created () {
        this.loadAssignments()
    }
}
</script>
