<template>
    <content-single-column>
        <bread-crumb :currentPage="'Assignments'"></bread-crumb>

        <b-card class="no-hover">
                <b-row>
                    <b-col sm="6">
                        <b-form-select v-model="selectedSortOption" :select-size="1">
                           <option value="sortDate">Sort by date</option>
                           <option value="sortName">Sort by name</option>
                           <option v-if="this.$root.canAddCourse()"
                                   value="sortNeedsMarking">Sort by marking needed</option>
                        </b-form-select>
                    </b-col>
                    <b-col sm="6">
                        <input class="theme-input full-width" type="text" v-model="searchVariable" placeholder="Search..."/>
                    </b-col>
                </b-row>
        </b-card>

        <div v-for="(d, i) in computedDeadlines" :key="i">
            <b-link tag="b-button" :to="assignmentRoute(d.cID, d.aID, d.jID)">
                <todo-card
                    :deadline="d.deadline"
                    :name="d.name"
                    :abbr="d.courseAbbr"
                    :totalNeedsMarking="d.totalNeedsMarking"
                    :class="$root.getBorderClass(d.cID)">
                </todo-card>
            </b-link>
        </div>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import mainCard from '@/components/assets/MainCard.vue'
import assignmentApi from '@/api/assignment.js'
import todoCard from '@/components/assets/TodoCard.vue'

export default {
    name: 'AssignmentsOverview',
    data () {
        return {
            deadlines: [],
            selectedSortOption: 'sortDate',
            searchVariable: ''

        }
    },
    created () {
        assignmentApi.get_upcoming_deadlines()
            .then(deadlines => { this.deadlines = deadlines })
            .catch(error => { this.$toasted.error(error.response.data.description) })
    },
    components: {
        'content-single-column': contentSingleColumn,
        'bread-crumb': breadCrumb,
        'main-card': mainCard,
        'todo-card': todoCard
    },
    methods: {
        assignmentRoute (cID, aID, jID) {
            var route = {
                name: 'Assignment',
                params: {
                    cID: cID,
                    aID: aID
                }
            }

            if (jID) {
                route.params.jID = jID
            }

            return route
        }
    },
    computed: {
        computedDeadlines: function () {
            let self = this

            function compareName (a, b) {
                if (a.name < b.name) { return -1 }
                if (a.name > b.name) { return 1 }
                return 0
            }

            function compareDate (a, b) {
                return new Date(a.deadline.Date) - new Date(b.deadline.Date)
            }

            function compareMarkingNeeded (a, b) {
                if (a.totalNeedsMarking > b.totalNeedsMarking) { return -1 }
                if (a.totalNeedsMarking < b.totalNeedsMarking) { return 1 }
                return 0
            }

            function searchFilter (assignment) {
                var searchVariable = self.searchVariable.toLowerCase()
                return (assignment.name.toLowerCase().includes(searchVariable) ||
                        assignment.courseAbbr.toLowerCase().includes(searchVariable))
            }

            if (this.selectedSortOption === 'sortName') {
                return this.deadlines.filter(searchFilter).slice().sort(compareName)
            } else if (this.selectedSortOption === 'sortDate') {
                return this.deadlines.filter(searchFilter).slice().sort(compareDate)
            } else if (this.selectedSortOption === 'sortNeedsMarking') {
                return this.deadlines.filter(searchFilter).slice().sort(compareMarkingNeeded)
            } else {
                return this.deadlines.filter(searchFilter).slice()
            }
        }
    }
}
</script>
