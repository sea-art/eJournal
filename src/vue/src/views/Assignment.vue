<template>
    <content-columns>
        <bread-crumb slot="main-content-column" @eye-click="customisePage" @edit-click="handleEdit()"/>
        <b-card slot="main-content-column" class="no-hover settings-card">
            <b-row>
                <b-col sm="6">
                    <b-form-select class="multi-form" v-model="selectedSortOption" :select-size="1">
                       <option value="sortName">Sort by name</option>
                       <option value="sortID">Sort by ID</option>
                       <option value="sortMarking">Sort by marking needed</option>
                    </b-form-select>
                </b-col>
                <b-col sm="6">
                    <input class="theme-input multi-form full-width" type="text" v-model="searchVariable" placeholder="Search .."/>
                </b-col>
            </b-row>
            <b-button
                v-if="$root.canGradeJournal()"
                class="add-button"
                @click="publishGradesAssignment">
                <icon name="upload"/>
                Publish all Grades for this Assignment
            </b-button>
        </b-card>

        <div v-if="assignmentJournals.length > 0" v-for="journal in filteredJournals" :key="journal.student.uID" slot="main-content-column">
            <b-link tag="b-button" :to="{ name: 'Journal',
                                          params: {
                                              cID: cID,
                                              aID: aID,
                                              jID: journal.jID
                                          }, query: query
                                        }">

                <student-card
                    :student="journal.student.first_name + ' ' + journal.student.last_name"
                    :studentNumber="journal.student.name"
                    :portraitPath="journal.student.picture"
                    :stats="journal.stats"
                    :jID="journal.jID">
                </student-card>

            </b-link>
        </div>
        <main-card slot="main-content-column" class="no-hover" :line1="'No journals found'"/>

        <div  v-if="stats" slot="right-content-column">
            <h3>Statistics</h3>
            <statistics-card :subject="'Needs marking'" :num="stats.needsMarking"></statistics-card>
            <statistics-card :subject="'Average points'" :num="stats.avgPoints"></statistics-card>
            <statistics-card :subject="'Median points'" :num="stats.medianPoints"></statistics-card>
            <statistics-card :subject="'Average entries'" :num="stats.avgEntries"></statistics-card>
        </div>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/columns/ContentColumns.vue'
import studentCard from '@/components/assignment/StudentCard.vue'
import mainCard from '@/components/assets/MainCard.vue'
import statisticsCard from '@/components/assignment/StatisticsCard.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import journal from '@/api/journal.js'
import permissionsApi from '@/api/permissions.js'
import store from '@/Store.vue'
import icon from 'vue-awesome/components/Icon'

export default {
    name: 'Assignment',
    props: {
        cID: {
            required: true
        },
        aID: {
            required: true
        },
        assignmentName: ''
    },
    data () {
        return {
            assignmentJournals: [],
            stats: [],
            selectedSortOption: 'sortName',
            searchVariable: '',
            query: {}
        }
    },
    components: {
        'content-columns': contentColumns,
        'student-card': studentCard,
        'statistics-card': statisticsCard,
        'bread-crumb': breadCrumb,
        'store': store,
        'icon': icon,
        'main-card': mainCard
    },
    created () {
        permissionsApi.get_course_permissions(this.cID)
            .then(response => {
                if (!this.$router.app.canViewAssignmentParticipants()) {
                    this.$router.push({name: 'Course', params: {cID: this.cID}})
                    return
                }

                journal.get_assignment_journals(this.aID)
                    .then(response => {
                        this.assignmentJournals = response.journals
                        this.stats = response.stats
                    })
            })

        if (this.$route.query.sort === 'sortName' ||
            this.$route.query.sort === 'sortID' ||
            this.$route.query.sort === 'sortMarking') {
            this.selectedSortOption = this.$route.query.sort
        }

        if (this.$route.query.search) {
            this.searchVariable = this.$route.query.search
        }
    },
    methods: {
        customisePage () {
            this.$toasted.info('Wishlist: Customise page')
        },
        handleEdit () {
            this.$router.push({
                name: 'AssignmentEdit',
                params: {
                    cID: this.cID,
                    aID: this.aID
                }
            })
        },
        publishGradesAssignment () {
            if (confirm('Are you sure you want to publish all grades for each journal?')) {
                journal.update_publish_grades_assignment(this.aID, 1)
                    .then(_ => {
                        this.$toasted.success('Published all grades for this assignment.')
                    })
                    .catch(_ => {
                        this.$toasted.error('Error while publishing all grades for this assignment.')
                    })
            }
        },
        updateQuery () {
            if (this.searchVariable !== '') {
                this.query = {sort: this.selectedSortOption, search: this.searchVariable}
            } else {
                this.query = {sort: this.selectedSortOption}
            }

            this.$router.replace({ query: this.query })
        }
    },
    computed: {
        filteredJournals: function () {
            let self = this

            function compareName (a, b) {
                if (a.student.last_name < b.student.last_name) { return -1 }
                if (a.student.last_name > b.student.last_name) { return 1 }
                return 0
            }

            function compareID (a, b) {
                if (a.student.name < b.student.name) { return -1 }
                if (a.student.name > b.student.name) { return 1 }
                return 0
            }

            function compareMarkingNeeded (a, b) {
                if (a.stats.submitted - a.stats.graded > b.stats.submitted - b.stats.graded) { return -1 }
                if (a.stats.submitted - a.stats.graded < b.stats.submitted - b.stats.graded) { return 1 }
                return 0
            }

            function checkFilter (user) {
                var userName = (user.student.first_name + ' ' + user.student.lastname).toLowerCase()
                var userID = user.student.name.toLowerCase()

                if (userName.includes(self.searchVariable.toLowerCase()) ||
                userID.includes(self.searchVariable)) {
                    return true
                } else {
                    return false
                }
            }

            /* Filter list based on search input. */
            if (this.selectedSortOption === 'sortName') {
                store.setFilteredJournals(this.assignmentJournals.filter(checkFilter).sort(compareName))
            } else if (this.selectedSortOption === 'sortID') {
                store.setFilteredJournals(this.assignmentJournals.filter(checkFilter).sort(compareID))
            } else if (this.selectedSortOption === 'sortMarking') {
                store.setFilteredJournals(this.assignmentJournals.filter(checkFilter).sort(compareMarkingNeeded))
            }

            this.updateQuery()

            return store.state.filteredJournals.slice()
        }
    }
}
</script>
