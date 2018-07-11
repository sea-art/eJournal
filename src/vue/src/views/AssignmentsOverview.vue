<template>
    <content-columns>
        <bread-crumb slot="main-content-column" :currentPage="'Assignments'"></bread-crumb>

        <b-card class="no-hover" slot="main-content-column">
                <b-row>
                    <b-col lg="4" sm="6">
                        <b-form-select v-model="selectedSortOption" :select-size="1">
                           <option :value="null">Sort by ...</option>
                           <option value="sortDate">Sort by date</option>
                           <option value="sortName">Sort by name</option>
                           <option v-if="this.$root.canAddCourse()"
                                   value="sortNeedsMarking">Sort by markings needed</option>
                        </b-form-select>
                    </b-col>
                    <b-col cols="6">
                        <input type="text" v-model="searchVariable" placeholder="Search .."/>
                    </b-col>
                </b-row>
        </b-card>

        <div v-for="(d, i) in computedDeadlines" :key="i" slot="main-content-column">
            <b-link tag="b-button" :to="journalRoute(d.cID, d.aID, d.jID, d.name)">
                <todo-card
                    :date="d.deadline.Date"
                    :hours="d.deadline.Hours"
                    :minutes="d.deadline.Minutes"
                    :name="d.name"
                    :abbr="d.courseAbbr"
                    :totalNeedsMarking="d.totalNeedsMarking"
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
import assignmentApi from '@/api/assignment.js'
import todoCard from '@/components/TodoCard.vue'

export default {
    name: 'AssignmentsOverview',
    data () {
        return {
            deadlines: [],
            selectedSortOption: null,
            searchVariable: ''

        }
    },
    created () {
        assignmentApi.get_upcoming_deadlines()
            .then(response => {
                this.deadlines = response
            })
            .catch(_ => this.$toasted.error('Error while loading deadlines'))
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
            let self = this

            function compareName (a, b) {
                if (a.name < b.name) { return -1 }
                if (a.name > b.name) { return 1 }
                return 0
            }

            function compareDate (a, b) {
                return new Date(a.deadline.Date) - new Date(b.deadline.Date)
            }

            function compareMarkingsNeeded (a, b) {
                if (a.totalNeedsMarking > b.totalNeedsMarking) { return -1 }
                if (a.totalNeedsMarking < b.totalNeedsMarking) { return 1 }
                return 0
            }

            function searchFilter (course) {
                return course.name.toLowerCase().includes(self.searchVariable.toLowerCase())
            }

            if (this.selectedSortOption === 'sortName') {
                return this.deadlines.filter(searchFilter).slice().sort(compareName)
            } else if (this.selectedSortOption === 'sortDate') {
                return this.deadlines.filter(searchFilter).slice().sort(compareDate)
            } else if (this.selectedSortOption === 'sortNeedsMarking') {
                return this.deadlines.filter(searchFilter).slice().sort(compareMarkingsNeeded)
            } else {
                return this.deadlines.filter(searchFilter).slice()
            }
        }
    }
}
</script>
