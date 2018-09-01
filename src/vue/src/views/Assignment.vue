<!-- TODO Is this check really required if we redirect, or even better have correct flow anyway? -->
<template v-if="$hasPermission('can_view_assignment_participants')">
    <content-columns>
        <bread-crumb slot="main-content-column" @eye-click="customisePage" @edit-click="handleEdit()"/>
        <b-card slot="main-content-column" class="no-hover settings-card">
            <b-row>
                <b-col sm="6">
                    <b-form-select class="multi-form" v-model="selectedSortOption" :select-size="1">
                       <option value="sortFullName">Sort by name</option>
                       <option value="sortUsername">Sort by username</option>
                       <option value="sortMarking">Sort by marking needed</option>
                    </b-form-select>
                </b-col>
                <b-col sm="6">
                    <input class="theme-input multi-form full-width" type="text" v-model="searchVariable" placeholder="Search..."/>
                </b-col>
            </b-row>
            <b-button
                v-if="$hasPermission('can_publish_assignment_grades')"
                class="add-button"
                @click="publishGradesAssignment">
                <icon name="upload"/>
                Publish all Grades for this Assignment
            </b-button>
        </b-card>

        <div v-if="filteredJournals" v-for="journal in filteredJournals" :key="journal.student.id" slot="main-content-column">
            <b-link tag="b-button" :to="{ name: 'Journal',
                                          params: {
                                              cID: cID,
                                              aID: aID,
                                              jID: journal.id
                                          }, query: query
                                        }">

                <student-card
                    :student="journal.student"
                    :stats="journal.stats">
                </student-card>
            </b-link>
        </div>
        <main-card v-else slot="main-content-column" class="no-hover" :line1="'No journals found'"/>

        <div v-if="stats" slot="right-content-column">
            <h3>Insights</h3>
            <statistics-card :subject="'Needs marking'" :num="stats.needs_marking"></statistics-card>
            <statistics-card :subject="'Average points'" :num="stats.average_points"></statistics-card>
        </div>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/columns/ContentColumns.vue'
import studentCard from '@/components/assignment/StudentCard.vue'
import mainCard from '@/components/assets/MainCard.vue'
import statisticsCard from '@/components/assignment/StatisticsCard.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'

import store from '@/Store.vue'
import assignmentAPI from '@/api/assignment'
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
        jID: 0
    },
    data () {
        return {
            assignmentJournals: [],
            stats: [],
            selectedSortOption: 'sortUsername',
            searchVariable: '',
            query: {}
        }
    },
    components: {
        'content-columns': contentColumns,
        'student-card': studentCard,
        'statistics-card': statisticsCard,
        'bread-crumb': breadCrumb,
        store,
        icon,
        'main-card': mainCard
    },
    created () {
        assignmentAPI.get(this.aID, this.cID)
            .then(data => {
                this.assignmentJournals = data.journals
                this.stats = data.stats
            })
            .catch(error => {
                this.$toasted.error(error.response.data.description)
            })

        if (this.$route.query.sort === 'sortFullName' ||
            this.$route.query.sort === 'sortUsername' ||
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
                alert('Not implemented yet')
                // journal.update_publish_grades_assignment(this.aID, 1)
                //     .then(_ => {
                //         this.$toasted.success('Published all grades for this assignment.')
                //         journal.get_assignment_journals(this.aID)
                //             .then(response => {
                //                 this.assignmentJournals = response.journals
                //                 this.stats = response.stats
                //             })
                //     })
                //     .catch(_ => {
                //         this.$toasted.error('Error while publishing all grades for this assignment.')
                //     })
            }
        },
        updateQuery () {
            if (this.searchVariable !== '') {
                this.query = {sort: this.selectedSortOption, search: this.searchVariable}
            } else {
                this.query = {sort: this.selectedSortOption}
            }

            if (this.$route.query !== this.query) {
                this.$router.replace({ query: this.query })
            }
        }
    },
    computed: {
        filteredJournals: function () {
            let self = this

            function compareFullName (a, b) {
                var fullNameA = a.student.first_name + ' ' + a.student.last_name
                var fullNameB = b.student.first_name + ' ' + b.student.last_name

                if (fullNameA < fullNameB) { return -1 }
                if (fullNameA > fullNameB) { return 1 }
                return 0
            }

            function compareUsername (a, b) {
                if (a.student.username < b.student.username) { return -1 }
                if (a.student.username > b.student.username) { return 1 }
                return 0
            }

            function compareMarkingNeeded (a, b) {
                if (a.stats.submitted - a.stats.graded < b.stats.submitted - b.stats.graded) { return -1 }
                if (a.stats.submitted - a.stats.graded > b.stats.submitted - b.stats.graded) { return 1 }
                return 0
            }

            function checkFilter (user) {
                var username = user.student.username.toLowerCase()
                var fullName = user.student.first_name.toLowerCase() + ' ' + user.student.last_name.toLowerCase()
                var searchVariable = self.searchVariable.toLowerCase()

                if (username.includes(searchVariable) ||
                    fullName.includes(searchVariable)) {
                    return true
                } else {
                    return false
                }
            }

            /* Filter list based on search input. */
            if (this.selectedSortOption === 'sortFullName') {
                store.setFilteredJournals(this.assignmentJournals.filter(checkFilter).sort(compareFullName))
            } else if (this.selectedSortOption === 'sortUsername') {
                store.setFilteredJournals(this.assignmentJournals.filter(checkFilter).sort(compareUsername))
            } else if (this.selectedSortOption === 'sortMarking') {
                store.setFilteredJournals(this.assignmentJournals.filter(checkFilter).sort(compareMarkingNeeded))
            }

            this.updateQuery()

            return store.state.filteredJournals.slice()
        }
    }
}
</script>
