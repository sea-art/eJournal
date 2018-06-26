<template>
    <content-columns>
        <bread-crumb slot="main-content-column" @eye-click="customisePage" @edit-click="handleEdit()"/>
        <b-button slot="main-content-column" :to="{ name: 'FormatEdit', params: { cID: cID, aID: aID } }">Edit Assignment Format</b-button>
        <b-card slot="main-content-column" class="settings-card no-hover">
            <b-row>
                <b-col lg="3" md="3">
                    <b-form-select v-model="selectedSortOption" :select-size="1">
                       <option :value="null">Sort by ...</option>
                       <option value="sortName">Sort on name</option>
                       <option value="sortID">Sort on ID</option>
                    </b-form-select>
                </b-col>
                <b-col lg="3" md="3">
                    <input type="text" v-model="searchVariable" placeholder="Search .."/>
                </b-col>
            </b-row>
        </b-card>

        <div v-if="assignmentJournals.length > 0" v-for="journal in filteredJournals" :key="journal.student.uID" slot="main-content-column">
            <b-link tag="b-button" :to="{ name: 'Journal',
                                          params: {
                                              cID: cID,
                                              aID: aID,
                                              jID: journal.jID
                                          }
                                        }">
                <student-card
                    :student="journal.student.name"
                    :studentNumber="journal.student.uID"
                    :portraitPath="journal.student.picture"
                    :stats="journal.stats"
                    :color="$root.colors[journal.uid % $root.colors.length]">
                </student-card>
            </b-link>
        </div>
        <div v-if="assignmentJournals.length === 0" slot="main-content-column">
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
import journal from '@/api/journal.js'
// TODO: temp
import assignment from '@/api/assignment.js'

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
            selectedSortOption: null,
            searchVariable: ''
        }
    },
    components: {
        'content-columns': contentColumns,
        'student-card': studentCard,
        'statistics-card': statisticsCard,
        'bread-crumb': breadCrumb
    },
    created () {
        // TODO: Remove... just for demo
        if (!this.$root.canViewAssignmentParticipants()) {
            assignment.get_assignment_data(this.cID, this.aID)
                .then(data => {
                    this.$router.push({
                        name: 'Journal',
                        params: {
                            cID: this.cID,
                            aID: this.aID,
                            jID: data.journal.jID,
                            assignmentName: data.name
                        }})
                })
            return
        }

        journal.get_assignment_journals(this.aID)
            .then(response => {
                this.assignmentJournals = response.journals
                this.stats = response.stats
            })
            .catch(_ => alert('Error while loading jounals'))
    },
    methods: {
        customisePage () {
            alert('Wishlist: Customise page')
        },
        handleEdit () {
            this.$router.push({
                name: 'AssignmentEdit',
                params: {
                    cID: this.cID,
                    aID: this.aID
                }
            })
        }
    },
    computed: {
        filteredJournals: function () {
            let self = this

            function compareName (a, b) {
                if (a.student.name < b.student.name) { return -1 }
                if (a.student.name > b.student.name) { return 1 }
                return 0
            }

            function compareID (a, b) {
                if (a.student.uID < b.student.uID) { return -1 }
                if (a.student.uID > b.student.uID) { return 1 }
                return 0
            }

            function checkFilter (user) {
                var userName = user.student.name.toLowerCase()
                var userID = String(user.student.uID).toLowerCase()

                if (userName.includes(self.searchVariable.toLowerCase()) ||
                userID.includes(self.searchVariable)) {
                    return true
                } else {
                    return false
                }
            }

            /* Filter list based on search input. */
            if (this.selectedSortOption === 'sortName') {
                return this.assignmentJournals.filter(checkFilter).sort(compareName)
            } else if (this.selectedSortOption === 'sortID') {
                return this.assignmentJournals.filter(checkFilter).sort(compareID)
            } else {
                return this.assignmentJournals.filter(checkFilter)
            }
        }
    }
}
</script>
