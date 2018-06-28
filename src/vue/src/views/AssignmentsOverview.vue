<template>
    <content-columns>
        <bread-crumb slot="main-content-column" :currentPage="'Assignments'"></bread-crumb>

        <div v-for="(d, i) in computedDeadlines" :key="i" slot="main-content-column">
            <b-link tag="b-button" :to="journalRoute(d.cID, d.aID, d.jID, d.name)">
                <todo-card
                    :date="d.deadline.Date"
                    :hours="d.deadline.Hours"
                    :minutes="d.deadline.Minutes"
                    :name="d.name"
                    :abbr="d.courseAbbr"
                    :color="$root.colors[d.cID % $root.colors.length]">
                </todo-card>
            </b-link>
        </div>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
import mainCard from '@/components/MainCard.vue'
import assignmentApi from '@/assignment.js'
import todoCard from '@/components/TodoCard.vue'

export default {
    name: 'AssignmentsOverview',
    data () {
        return {
            deadlines: []
        }
    },
    created () {
        assignmentApi.get_upcoming_deadlines()
            .then(response => {
                this.deadlines = response
            })
            .catch(_ => alert('Error while loading deadlines'))
    },
    components: {
        'content-columns': contentColumns,
        'bread-crumb': breadCrumb,
        'main-card': mainCard,
        'todo-card': todoCard
    },
    methods: {
        journalRoute (cID, aID, jID, name) {
            if (this.$root.canAddCourse()) {
                return {
                    name: 'Assignment',
                    params: {
                        cID: cID,
                        aID: aID,
                        assignmentName: name
                    }
                }
            } else {
                return {
                    name: 'Journal',
                    params: {
                        cID: cID,
                        aID: aID,
                        jID: jID,
                        assignmentName: name
                    }
                }
            }
        }
    },
    computed: {
        computedDeadlines: function () {
            function compareDate (a, b) {
                return new Date(a.deadline.Date) - new Date(b.deadline.Date)
            }

            return this.deadlines.slice().sort(compareDate)
        }
    }
}
</script>
