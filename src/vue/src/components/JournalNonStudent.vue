<template>
    <b-row class="outer-container" no-gutters>
        <b-col v-if="bootstrapLg()" cols="12">
            <bread-crumb v-if="bootstrapLg()" :currentPage="$route.params.assignmentName" :course="$route.params.courseName">&nbsp;</bread-crumb>
            <edag @select-node="selectNode" :selected="currentNode" :nodes="nodes"/>
        </b-col>
        <b-col v-else xl="3" class="left-content-journal">
            <edag @select-node="selectNode" :selected="currentNode" :nodes="nodes"/>
        </b-col>

<b-col lg="12" xl="6" order="3" order-xl="2" class="main-content-journal">
            <bread-crumb v-if="!bootstrapLg()" :currentPage="$route.params.assignmentName" :course="$route.params.courseName">&nbsp;</bread-crumb>
            <div v-if="nodes.length > currentNode">
                <div v-if="nodes[currentNode].type == 'e'">
                    <entry-non-student-preview ref="entry-template-card" @check-grade="updatedGrade" :entryNode="nodes[currentNode]"/>
                </div>
                <div v-else-if="nodes[currentNode].type == 'd'">
                    <entry-non-student-preview v-if="nodes[currentNode].entry !== null" ref="entry-template-card" @check-grade="updatedGrade" :entryNode="nodes[currentNode]"/>
                    <div v-else>No entry yet submitted</div>
                </div>
                <div v-else-if="nodes[currentNode].type == 'p'">
                    <b-card class="card main-card no-hover" :class="'pink-border'">
                        <h2>Needed progress</h2>
                        Has reached {{progressNodes[nodes[currentNode].nID]}} points out of the {{nodes[currentNode].target}}
                        before {{nodes[currentNode].deadline}}.
                    </b-card>
                </div>
            </div>
        </b-col>
        <b-col cols="12" xl="3" order="2" order-xl="3" class="right-content-journal">
            <h3>Journal</h3>
            <b-card class="no-hover">
                <b-button tag="b-button" v-if="filteredJournals.length !== 0" :to="{ name: 'Journal',
                                              params: {
                                                  cID: cID,
                                                  aID: aID,
                                                  jID: prevJournal.jID
                                              },
                                              query: query
                                            }">
                    Previous
                </b-button>
                <b-button tag="b-button" v-if="filteredJournals.length !== 0" :to="{ name: 'Journal',
                                              params: {
                                                  cID: cID,
                                                  aID: aID,
                                                  jID: nextJournal.jID
                                              },
                                              query: query
                                            }">
                    Next
                </b-button>
                <!-- {{ filteredJournals }} -->
                <b-button @click="publishGradesJournal">Publish Grades</b-button>
            </b-card>
        </b-col>
    </b-row>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import entryNonStudentPreview from '@/components/EntryNonStudentPreview.vue'
import addCard from '@/components/AddCard.vue'
import edag from '@/components/Edag.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
import journal from '@/api/journal'
import store from '@/Store.vue'

export default {
    props: ['cID', 'aID', 'jID'],
    data () {
        return {
            currentNode: 0,
            editedData: ['', ''],
            nodes: [],
            newNodes: [],
            progressNodes: {},
            assignmentJournals: [],
            selectedSortOption: 'sortName',
            searchVariable: '',
            query: {}
        }
    },
    created () {
        journal.get_nodes(this.jID)
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

        if (store.state.filteredJournals.length === 0) {
            alert($root.canEditJournal())
            journal.get_assignment_journals(2)
                .then(response => {
                    this.assignmentJournals = response.journals
                })

            if (this.$route.query.sort === 'sortName' ||
                this.$route.query.sort === 'sortID' ||
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
             * tree. */
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
            journal.create_entry(this.jID, infoEntry[0].tID, infoEntry[1])
                .then(_ => journal.get_nodes(this.jID)
                    .then(response => { this.nodes = response.nodes })
                    .catch(error => this.$toasted.error('Error while loading nodes.')))
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
                    if (node.entry.grade != null && node.entry.grade !== '0' && node.entry.published) {
                        tempProgress += parseInt(node.entry.grade)
                    }
                }
            }

            this.progressNodes[progressNode.nID] = tempProgress.toString()
        },
        updatedGrade () {
            for (var node of this.nodes) {
                if (node.type === 'p') {
                    this.progressPoints(node)
                }
            }
        },
        publishGradesJournal () {
            journal.update_publish_grades_journal(this.jID, 1)
                .then(_ => {
                    this.$toasted.success('All the grades for this journal are published.')
                })
                .catch(_ => {
                    this.$toasted.error('Error publishing all grades for this journal')
                })

            for (var node of this.nodes) {
                if (node.type === 'e' || node.type === 'd') {
                    node.entry.published = true
                }
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
        bootstrapLg () {
            return this.windowHeight < 1200
        },
        bootstrapMd () {
            return this.windowHeight < 922
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
                if (array[i][property] === value) {
                    return i
                }
            }

            return -1
        }
    },
    components: {
        'entry-non-student-preview': entryNonStudentPreview,
        'content-columns': contentColumns,
        'bread-crumb': breadCrumb,
        'add-card': addCard,
        'edag': edag,
        'store': store
    },
    computed: {
        filteredJournals: function () {
            let self = this

            // TODO: add better compare functions
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

            function compareMarkingNeeded (a, b) {
                if (a.stats.submitted - a.stats.graded < b.stats.submitted - b.stats.graded) { return -1 }
                if (a.stats.submitted - a.stats.graded > b.stats.submitted - b.stats.graded) { return 1 }
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

            if (store.state.filteredJournals.length === 0) {
                /* Filter list based on search input. */
                if (this.selectedSortOption === 'sortName') {
                    store.setFilteredJournals(this.assignmentJournals.filter(checkFilter).sort(compareName))
                } else if (this.selectedSortOption === 'sortID') {
                    store.setFilteredJournals(this.assignmentJournals.filter(checkFilter).sort(compareID))
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
