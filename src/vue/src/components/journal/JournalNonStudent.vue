<template>
    <b-row class="outer-container-timeline-page" no-gutters>
        <b-col md="12" lg="8" xl="9" class="inner-container-timeline-page">
            <b-col md="12" lg="auto" xl="4" class="left-content-timeline-page">
                <bread-crumb v-if="$root.lgMax()"></bread-crumb>
                <timeline @select-node="selectNode" :selected="currentNode" :nodes="nodes"/>
            </b-col>

            <b-col md="12" lg="auto" xl="8" class="main-content-timeline-page">
                <bread-crumb v-if="$root.xl()"></bread-crumb>
                <div v-if="nodes.length > currentNode && currentNode !== -1">
                    <div v-if="nodes[currentNode].type == 'e' || nodes[currentNode].type == 'd'">
                        <entry-non-student-preview ref="entry-template-card" @check-grade="updatedGrade" :entryNode="nodes[currentNode]"/>
                    </div>
                    <div v-else-if="nodes[currentNode].type == 'p'">
                        <progress-node :currentNode="nodes[currentNode]" :nodes="nodes"/>
                    </div>
                </div>
                <journal-start-card v-else-if="currentNode === -1" :assignment="assignment"/>
                <journal-end-card v-else :assignment="assignment"/>
            </b-col>
        </b-col>

        <b-col md="12" lg="4" xl="3" class="right-content-timeline-page right-content">
            <b-row>
                <b-col md="6" lg="12" class="mb-4">
                    <h3>Journal progress</h3>
                    <student-card
                        v-if="journal"
                        :student="journal.student"
                        :stats="journal.stats"
                        :assignment="assignment"
                        :class="'mb-2 no-hover'"/>
                    <div v-if="journal && $hasPermission('can_grade')">
                        <div v-if="$hasPermission('can_grade')" class="grade-section full-width bonus-section shadow">
                            <icon name="star" class="fill-orange shift-up-2"/>
                            <b-form-input type="number" class="theme-input mr-2" size="2" v-model="journal.bonus_points" placeholder="0" min="0.0"/> Bonus points
                            <b-button class="add-button" @click="commitBonus">
                                <icon name="save" scale="1"/>
                                Save Bonus
                            </b-button>
                        </div>
                    </div>
                </b-col>
                <b-col v-if="$hasPermission('can_publish_grades') || filteredJournals.length > 1" md="6" lg="12">
                    <h3>Controls</h3>
                    <div class="d-flex" v-if="filteredJournals.length > 1">
                        <b-button
                            class="multi-form mr-1 flex-grow-1"
                            tag="b-button"
                            v-if="filteredJournals.length !== 0"
                            :to="{ name: 'Journal', params: { cID: cID, aID: aID, jID: prevJournal.id } }">
                            <icon name="arrow-left"/>
                            Previous
                        </b-button>
                        <b-button
                            class="multi-form flex-grow-1"
                            tag="b-button"
                            v-if="filteredJournals.length !== 0"
                            :to="{ name: 'Journal', params: { cID: cID, aID: aID, jID: nextJournal.id } }">
                            Next
                            <icon name="arrow-right"/>
                        </b-button>
                    </div>
                    <b-button v-if="$hasPermission('can_publish_grades')" class="add-button flex-grow-1 full-width" @click="publishGradesJournal">
                        <icon name="upload"/>
                        Publish All Grades
                    </b-button>
                </b-col>
            </b-row>
        </b-col>
    </b-row>
</template>

<script>
import contentColumns from '@/components/columns/ContentColumns.vue'
import entryNonStudentPreview from '@/components/entry/EntryNonStudentPreview.vue'
import addCard from '@/components/journal/AddCard.vue'
import timeline from '@/components/timeline/Timeline.vue'
import studentCard from '@/components/assignment/StudentCard.vue'
import progressBar from '@/components/assets/ProgressBar.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import journalStartCard from '@/components/journal/JournalStartCard.vue'
import journalEndCard from '@/components/journal/JournalEndCard.vue'
import progressNode from '@/components/entry/ProgressNode.vue'

import icon from 'vue-awesome/components/Icon'
import store from '@/Store.vue'
import journalAPI from '@/api/journal'
import assignmentAPI from '@/api/assignment'
import { mapGetters, mapMutations } from 'vuex'

export default {
    props: ['cID', 'aID', 'jID'],
    data () {
        return {
            currentNode: -1,
            editedData: ['', ''],
            nodes: [],
            progressNodes: {},
            progressPointsLeft: 0,
            assignmentJournals: [],
            assignment: {},
            journal: null
        }
    },
    created () {
        this.switchJournalAssignment(this.aID)

        assignmentAPI.get(this.aID)
            .then(assignment => { this.assignment = assignment })
        journalAPI.getNodes(this.jID)
            .then(nodes => {
                this.nodes = nodes
                if (this.$route.query.nID !== undefined) {
                    this.currentNode = this.findEntryNode(parseInt(this.$route.query.nID))
                } else {
                    this.selectFirstUngradedNode()
                }
            })

        journalAPI.get(this.jID)
            .then(journal => { this.journal = journal })

        if (store.state.filteredJournals.length === 0) {
            if (this.$hasPermission('can_view_all_journals')) {
                journalAPI.getFromAssignment(this.cID, this.aID)
                    .then(journals => { this.assignmentJournals = journals })
            }
        }
    },
    methods: {
        ...mapMutations({
            switchJournalAssignment: 'preferences/SWITCH_JOURNAL_ASSIGNMENT'
        }),
        selectFirstUngradedNode () {
            var min = this.nodes.length - 1

            for (var i = 0; i < this.nodes.length; i++) {
                if ('entry' in this.nodes[i] && this.nodes[i].entry) {
                    let entry = this.nodes[i].entry
                    if (('grade' in entry && entry.grade === null) || ('published' in entry && !entry.published)) {
                        if (i < min) { min = i }
                    }
                }
            }

            if (min < this.nodes.length - 1) { this.currentNode = min }
        },
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

            if (!this.discardChanges()) {
                return
            }

            if (this.currentNode === -1 || this.currentNode === this.nodes.length ||
                this.nodes[this.currentNode].type !== 'e' ||
                this.nodes[this.currentNode].type !== 'd') {
                this.currentNode = $event
                return
            }

            if (this.$refs['entry-template-card'].saveEditMode === 'Save') {
                if (!confirm('Progress will not be saved if you leave. Do you wish to continue?')) {
                    return
                }
            }

            this.currentNode = $event
        },
        updatedGrade () {
            journalAPI.get(this.jID)
                .then(journal => { this.journal = journal })
        },
        publishGradesJournal () {
            if (confirm('Are you sure you want to publish all grades for this journal?')) {
                journalAPI.update(this.jID, {published: true}, {
                    customSuccessToast: 'Published all grades for this journal.',
                    customErrorToast: 'Error while publishing all grades for this journal.'
                })
                    .then(() => {
                        for (var node of this.nodes) {
                            if ((node.type === 'e' || node.type === 'd') && node.entry) {
                                node.entry.published = true
                            }
                        }

                        journalAPI.getNodes(this.jID)
                            .then(nodes => { this.nodes = nodes })
                        journalAPI.get(this.jID)
                            .then(journal => { this.journal = journal })
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
        findIndex (array, property, value) {
            for (var i = 0; i < array.length; i++) {
                if (String(array[i][property]) === String(value)) {
                    return i
                }
            }

            return false
        },
        compare (a, b) {
            if (a < b) { return -1 }
            if (a > b) { return 1 }
            return 0
        },
        discardChanges () {
            if (this.currentNode !== -1 && this.currentNode !== this.nodes.length && (this.nodes[this.currentNode].type === 'e' ||
                (this.nodes[this.currentNode].type === 'd' && this.nodes[this.currentNode].entry !== null))) {
                if ((this.$refs['entry-template-card'].grade !== this.nodes[this.currentNode].entry.grade ||
                    this.$refs['entry-template-card'].published !== this.nodes[this.currentNode].entry.published) &&
                    !confirm('Progress will not be saved if you leave. Do you wish to continue?')) {
                    return false
                }
            }

            return true
        },

        commitBonus () {
            if (this.journal.bonus_points !== null && this.journal.bonus_points !== '') {
                journalAPI.update(this.journal.id, {bonus_points: this.journal.bonus_points}, {customSuccessToast: 'Bonus succesfully added.'})
                    .then(journal => { this.journal = journal })
            }
        }
    },
    components: {
        'entry-non-student-preview': entryNonStudentPreview,
        'content-columns': contentColumns,
        'bread-crumb': breadCrumb,
        'add-card': addCard,
        timeline,
        store,
        'student-card': studentCard,
        icon,
        'progress-bar': progressBar,
        'journal-start-card': journalStartCard,
        'journal-end-card': journalEndCard,
        'progress-node': progressNode
    },
    computed: {
        ...mapGetters({
            getJournalSortBy: 'preferences/journalSortBy',
            order: 'preferences/journalSortAscending',
            getJournalSearchValue: 'preferences/journalSearchValue',
            getJournalGroupFilter: 'preferences/journalGroupFilter'
        }),
        filteredJournals: function () {
            let self = this

            function compareFullName (a, b) {
                return self.compare(a.student.full_name, b.student.full_name)
            }

            function compareUsername (a, b) {
                return self.compare(a.student.username, b.student.username)
            }

            function compareMarkingNeeded (a, b) {
                return self.compare(a.stats.submitted - a.stats.graded, b.stats.submitted - b.stats.graded)
            }

            function checkFilter (user) {
                var username = user.student.username.toLowerCase()
                var fullName = user.student.full_name
                var searchVariable = self.getJournalSearchValue.toLowerCase()

                return username.includes(searchVariable) ||
                       fullName.includes(searchVariable)
            }

            function groupFilter (assignment) {
                if (self.getJournalGroupFilter) {
                    return assignment.student.group === self.getJournalGroupFilter
                }

                return true
            }

            if (store.state.filteredJournals.length === 0) {
                /* Filter list based on search input. */
                if (this.getJournalSortBy === 'sortFullName') {
                    store.setFilteredJournals(this.assignmentJournals.filter(checkFilter).sort(compareFullName))
                } else if (this.getJournalSortBy === 'sortUsername') {
                    store.setFilteredJournals(this.assignmentJournals.filter(checkFilter).sort(compareUsername))
                } else if (this.getJournalSortBy === 'sortMarking') {
                    store.setFilteredJournals(this.assignmentJournals.filter(checkFilter).sort(compareMarkingNeeded))
                }
            }

            return store.state.filteredJournals.filter(groupFilter).slice()
        },
        prevJournal () {
            var curIndex = this.findIndex(this.filteredJournals, 'id', this.jID)
            var prevIndex = (curIndex - 1 + this.filteredJournals.length) % this.filteredJournals.length

            return this.filteredJournals[prevIndex]
        },
        nextJournal () {
            var curIndex = this.findIndex(this.filteredJournals, 'id', this.jID)
            var nextIndex = (curIndex + 1) % this.filteredJournals.length

            return this.filteredJournals[nextIndex]
        }
    }
}
</script>

<style lang="sass">
.bonus-section
    margin-bottom: 0px
    border-width: 3px !important
</style>
