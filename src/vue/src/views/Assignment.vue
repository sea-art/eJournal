<template>
    <content-columns>
        <bread-crumb slot="main-content-column" @eye-click="customisePage" @edit-click="handleEdit()"/>
        <b-card slot="main-content-column" class="settings-card no-hover">
            <b-row>
                <b-col lg="3" md="3">
                    <b-button
                        v-if="$root.canAddAssignment()"
                        class="change-button"
                        :to="{ name: 'FormatEdit', params: { cID: cID, aID: aID } }">
                        Edit Assignment Format
                    </b-button>
                </b-col>
            </b-row>
            <b-row>
                <b-col lg="3" md="3">
                    <b-form-select v-model="selectedSortOption" :select-size="1">
                       <option value="sortName">Sort by name</option>
                       <option value="sortID">Sort by ID</option>
                       <option value="sortMarking">Sort by marking needed</option>
                    </b-form-select>
                </b-col>
                <b-col lg="5" md="12">
                    <input type="text" v-model="searchVariable" placeholder="Search .."/>
                </b-col>
            </b-row>
            <b-row>
                <b-col lg="3" md="3">
                    <b-button
                        v-if="$root.canGradeJournal()"
                        class="add-button"
                        @click="publishGradesAssignment">
                        Publish all Grades
                    </b-button>
                </b-col>
            </b-row>
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
                    :color="$root.colors[cID % $root.colors.length]"
                    :jID="journal.jID">
                </student-card>

            </b-link>
        </div>
        <div v-else slot="main-content-column">
            <h1>No journals found</h1>
        </div>

        <div  v-if="stats" slot="right-content-column">
            <h3>Statistics</h3>
            <statistics-card :color="cardColor" :subject="'Needs marking'" :num="stats.needsMarking"></statistics-card>
            <statistics-card :color="cardColor" :subject="'Average points'" :num="stats.avgPoints"></statistics-card>
            <statistics-card :color="cardColor" :subject="'Median points'" :num="stats.medianPoints"></statistics-card>
            <statistics-card :color="cardColor" :subject="'Average entries'" :num="stats.avgEntries"></statistics-card>
        </div>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import studentCard from '@/components/StudentCard.vue'
import statisticsCard from '@/components/StatisticsCard.vue'
import breadCrumb from '@/components/BreadCrumb.vue'

import store from '@/Store.vue'
import auth from '@/api/auth'

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
            cardColor: '',
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
        'store': store
    },
    created () {
        auth.get('roles/' + this.cID)
            .then(response => {
                if (!this.$router.app.canViewAssignmentParticipants()) {
                    this.$router.push({name: 'Course', params: {cID: this.cID}})
                    return
                }

                auth.get('assignments/' + this.aID)
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
                        this.$toasted.success('All the grades for each journal are published.')
                    })
                    .catch(_ => {
                        this.$toasted.error('Error while publishing the grades for each journal.')
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
