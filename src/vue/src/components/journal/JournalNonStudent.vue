<template>
    <b-row class="outer-container-edag-page" no-gutters>
        <b-col md="12" lg="8" xl="9" class="inner-container-edag-page">
            <b-col md="12" lg="auto" xl="4" class="left-content-edag-page">
                <bread-crumb v-if="$root.lgMax()" class="main-content">&nbsp;</bread-crumb>
                <edag @select-node="selectNode" :selected="currentNode" :nodes="nodes"/>
            </b-col>

            <b-col md="12" lg="auto" xl="8" class="main-content-edag-page">
                <bread-crumb v-if="$root.xl()" class="main-content">&nbsp;</bread-crumb>
                <div v-if="nodes.length > currentNode">
                    <div v-if="nodes[currentNode].type == 'e' || nodes[currentNode].type == 'd'">
                        <entry-non-student-preview ref="entry-template-card" @check-grade="updatedGrade" :entryNode="nodes[currentNode]"/>
                    </div>
                    <div v-else-if="nodes[currentNode].type == 'p'">
                        <b-card class="no-hover" :class="getProgressBorderClass()">
                            <h2 class="mb-2">Progress: {{ nodes[currentNode].target }} points</h2>
                            <span v-if="progressPointsLeft > 0">
                                <b>{{ progressNodes[nodes[currentNode].nID] }}</b> out of <b>{{ nodes[currentNode].target }}</b> points.<br/>
                                <b>{{ progressPointsLeft }}</b> more required before <b>{{ $root.beautifyDate(nodes[currentNode].deadline) }}</b>.
                            </span>
                        </b-card>
                    </div>
                </div>
            </b-col>
        </b-col>

        <b-col md="12" lg="4" xl="3" class="right-content-edag-page right-content">
            <b-row>
                <b-col md="6" lg="12">
                    <h3>Journal</h3>
                    <student-card
                        v-if="journal"
                        :student="journal.student"
                        :stats="journal.stats"
                        :hideTodo="true"
                        :fullWidthProgress="true"
                        :class="'mb-4'"/>
                </b-col>
                <b-col md="6" lg="12">
                    <h3>Controls</h3>
                    <b-card class="no-hover settings-card" :class="$root.getBorderClass($route.params.cID)">
                        <div class="d-flex">
                            <b-button
                                class="multi-form flex-grow-1"
                                tag="b-button"
                                v-if="filteredJournals.length !== 0"
                                :to="{ name: 'Journal', params: { cID: cID, aID: aID, jID: prevJournal.jID }, query: query }">
                                <icon name="arrow-left"/>
                                Previous
                            </b-button>
                            <b-button
                                class="multi-form flex-grow-1"
                                tag="b-button"
                                v-if="filteredJournals.length !== 0"
                                :to="{ name: 'Journal', params: { cID: cID, aID: aID, jID: nextJournal.jID }, query: query }">
                                Next
                                <icon name="arrow-right"/>
                            </b-button>
                        </div>
                        <b-button v-if="this.$root.canPublishAssignmentGrades()" class="add-button flex-grow-1 full-width" @click="publishGradesJournal">
                            <icon name="upload"/>
                            Publish All Grades
                        </b-button>
                    </b-card>
                </b-col>
            </b-row>
        </b-col>
    </b-row>
</template>

<script>
import contentColumns from '@/components/columns/ContentColumns.vue'
import entryNonStudentPreview from '@/components/entry/EntryNonStudentPreview.vue'
import addCard from '@/components/journal/AddCard.vue'
import edag from '@/components/edag/Edag.vue'
import studentCard from '@/components/assignment/StudentCard.vue'
import icon from 'vue-awesome/components/Icon'
import progressBar from '@/components/assets/ProgressBar.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import journalApi from '@/api/journal'
import store from '@/Store.vue'

export default {
    props: ['cID', 'aID', 'jID'],
    data () {
        return {
            currentNode: 0,
            editedData: ['', ''],
            nodes: [],
            progressNodes: {},
            progressPointsLeft: 0,
            assignmentJournals: [],
            journal: null,
            selectedSortOption: 'sortUserName',
            searchVariable: '',
            query: {}
        }
    },
    created () {
        journalApi.get_nodes(this.jID)
            .then(response => {
                this.nodes = response.nodes
                if (this.$route.query.nID !== undefined) {
                    this.currentNode = this.findEntryNode(parseInt(this.$route.query.nID))
                }

                for (var node of this.nodes) {
                    if (node.type === 'p') {
                        this.progressPoints(node)
                    }
                }
            })

        journalApi.get_journal(this.jID)
            .then(response => {
                this.journal = response.journal
            })

        if (store.state.filteredJournals.length === 0) {
            if (this.$router.app.canViewAssignmentParticipants()) {
                journalApi.get_assignment_journals(this.aID)
                    .then(response => {
                        this.assignmentJournals = response.journals
                    })
            }

            if (this.$route.query.sort === 'sortFullName' ||
                this.$route.query.sort === 'sortUsername' ||
                this.$route.query.sort === 'sortMarking') {
                this.selectedSortOption = this.$route.query.sort
            }

            if (this.$route.query.search) {
                this.searchVariable = this.$route.query.search
            }
        }

        this.query = this.$route.query
    },
    watch: {
        currentNode: function () {
            if (this.nodes[this.currentNode].type === 'p') {
                this.progressPoints(this.nodes[this.currentNode])
                this.progressPointsLeft = this.nodes[this.currentNode].target - this.progressNodes[this.nodes[this.currentNode].nID]
            }
        }
    },
    methods: {
        adaptData (editedData) {
            this.nodes[this.currentNode] = editedData
        },
        selectNode ($event) {
            /* Function that prevents you from instant leaving an EntryNode
             * or a DeadlineNode when clicking on a different node in the
             * timeline. */
            if ($event === this.currentNode) {
                return this.currentNode
            }

            if (this.nodes[this.currentNode].type !== 'e' || this.nodes[this.currentNode].type !== 'd') {
                this.currentNode = $event
                return
            }

            if (this.$refs['entry-template-card'].saveEditMode === 'Save') {
                if (!confirm('Progress will not be saved if you leave. Do you wish to continue?')) {
                    return
                }
            }

            this.$refs['entry-template-card'].cancel()
            this.currentNode = $event
        },
        addNode (infoEntry) {
            journalApi.create_entry(this.jID, infoEntry[0].tID, infoEntry[1])
                .then(_ => journalApi.get_nodes(this.jID)
                    .then(response => { this.nodes = response.nodes })
                    .catch(_ => this.$toasted.error('Error while loading nodes.')))
        },
        progressPoints (progressNode) {
            /* The function will update a given progressNode by
             * going through all the nodes and count the published grades
             * so far. */
            var tempProgress = 0

            for (var node of this.nodes) {
                if (node.nID === progressNode.nID) {
                    break
                }

                if (node.type === 'e' || node.type === 'd') {
                    if (node.entry && node.entry.grade && node.entry.published && node.entry.grade !== '0') {
                        tempProgress += parseInt(node.entry.grade)
                    }
                }
            }

            this.progressNodes[progressNode.nID] = tempProgress.toString()
        },
        getProgressBorderClass () {
            return this.progressPointsLeft > 0 ? 'red-border' : 'green-border'
        },
        updatedGrade () {
            for (var node of this.nodes) {
                if (node.type === 'p') {
                    this.progressPoints(node)
                }
            }

            journalApi.get_journal(this.jID)
                .then(response => {
                    this.journal = response.journal
                })
        },
        publishGradesJournal () {
            if (confirm('Are you sure you want to publish all grades for this journal?')) {
                journalApi.update_publish_grades_journal(this.jID, 1)
                    .then(_ => {
                        this.$toasted.success('Published all grades for this journal.')

                        for (var node of this.nodes) {
                            if ((node.type === 'e' || node.type === 'd') && node.entry) {
                                node.entry.published = true
                            }
                        }

                        journalApi.get_nodes(this.jID)
                            .then(response => {
                                this.nodes = response.nodes
                            })

                        journalApi.get_journal(this.jID)
                            .then(response => {
                                this.journal = response.journal
                            })
                    })
                    .catch(_ => {
                        this.$toasted.error('Error while publishing all grades for this journal.')
                    })
            }
        },
        findEntryNode (nodeID) {
            for (var i = 0; i < this.nodes.length; i++) {
                if (this.nodes[i].nID === nodeID) {
                    return i
                }
            }
            return 0
        },
        updateQuery () {
            if (this.searchVariable !== '') {
                this.query = {sort: this.selectedSortOption, search: this.searchVariable}
            } else {
                this.query = {sort: this.selectedSortOption}
            }

            this.$router.replace({ query: this.query })
        },
        findIndex (array, property, value) {
            for (var i = 0; i < array.length; i++) {
                if (String(array[i][property]) === String(value)) {
                    return i
                }
            }

            return false
        }
    },
    components: {
        'entry-non-student-preview': entryNonStudentPreview,
        'content-columns': contentColumns,
        'bread-crumb': breadCrumb,
        'add-card': addCard,
        'edag': edag,
        'store': store,
        'student-card': studentCard,
        'icon': icon,
        'progress-bar': progressBar
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

            if (store.state.filteredJournals.length === 0) {
                /* Filter list based on search input. */
                if (this.selectedSortOption === 'sortFullName') {
                    store.setFilteredJournals(this.assignmentJournals.filter(checkFilter).sort(compareFullName))
                } else if (this.selectedSortOption === 'sortUsername') {
                    store.setFilteredJournals(this.assignmentJournals.filter(checkFilter).sort(compareUsername))
                } else if (this.selectedSortOption === 'sortMarking') {
                    store.setFilteredJournals(this.assignmentJournals.filter(checkFilter).sort(compareMarkingNeeded))
                }

                this.updateQuery()
            }

            return store.state.filteredJournals.slice()
        },
        prevJournal () {
            var curIndex = this.findIndex(this.filteredJournals, 'jID', this.jID)
            var prevIndex = (curIndex - 1 + this.filteredJournals.length) % this.filteredJournals.length

            return this.filteredJournals[prevIndex]
        },
        nextJournal () {
            var curIndex = this.findIndex(this.filteredJournals, 'jID', this.jID)
            var nextIndex = (curIndex + 1) % this.filteredJournals.length

            return this.filteredJournals[nextIndex]
        }

    }
}
</script>
