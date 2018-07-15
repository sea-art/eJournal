<template>
    <content-columns>
        <bread-crumb
            slot="main-content-column"
            @eye-click="customisePage"
            @edit-click="handleEdit()"/>

        <div slot="main-content-column" v-for="a in assignments" :key="a.aID">
            <b-link tag="b-button" :to="assignmentRoute(cID, a.aID, a.name, a.journal)">
                <assignment-card :line1="a.name">
                    <progress-bar
                        v-if="a.journal && a.journal.stats"
                        :currentPoints="a.journal.stats.acquired_points"
                        :totalPoints="a.journal.stats.total_points"/>
                </assignment-card>
            </b-link>
        </div>

        <main-card slot="main-content-column" v-if="$root.canAddAssignment()" class="add-card" v-on:click.native="showModal('createAssignmentRef')" :line1="'+ Add assignment'"/>

        <h3 slot="right-content-column">Upcoming</h3>

        <b-card v-if="this.$root.canViewAssignmentParticipants()"
                class="no-hover"
                slot="right-content-column">
                <b-row>
                    <b-col lg="6" sm="6">
                        <b-form-select v-model="selectedSortOption" :select-size="1">
                           <option :value="null">Sort by ...</option>
                           <option value="sortDate">Sort by date</option>
                           <option value="sortNeedsMarking">Sort by markings needed</option>
                        </b-form-select>
                    </b-col>
                </b-row>
        </b-card>

        <div v-for="(d, i) in computedDeadlines" :key="i" slot="right-content-column">
            <b-link tag="b-button" :to="journalRoute(d.cID, d.aID, d.jID, d.name)">
                <todo-card
                    :date="d.deadline.Date"
                    :hours="d.deadline.Hours"
                    :minutes="d.deadline.Minutes"
                    :name="d.name"
                    :abbr="d.courseAbbr"
                    :totalNeedsMarking="d.totalNeedsMarking">
                </todo-card>
            </b-link>
        </div>
        <b-modal
            slot="main-content-column"
            ref="createAssignmentRef"
            title="Create assignment"
            size="lg"
            hide-footer>
                <create-assignment @handleAction="handleConfirm('createAssignmentRef')"></create-assignment>
        </b-modal>

    </content-columns>
</template>

<script>
import contentColumns from '@/components/columns/ContentColumns.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import assignmentCard from '@/components/assignment/AssignmentCard.vue'
import todoCard from '@/components/assets/TodoCard.vue'
import progressBar from '@/components/assets/ProgressBar.vue'
import assignment from '@/api/assignment.js'
import mainCard from '@/components/assets/MainCard.vue'
import createAssignment from '@/components/assignment/CreateAssignment.vue'
import courseApi from '@/api/course.js'

export default {
    name: 'Course',
    props: {
        cID: {
            required: true
        },
        courseName: String
    },
    data () {
        return {
            assignments: null,
            cardColor: '',
            post: null,
            error: null,
            selectedSortOption: null,
            deadlines: [],
            needsMarkingStats: []
        }
    },
    components: {
        'content-columns': contentColumns,
        'bread-crumb': breadCrumb,
        'assignment-card': assignmentCard,
        'todo-card': todoCard,
        'progress-bar': progressBar,
        'main-card': mainCard,
        'create-assignment': createAssignment
    },
    created () {
        this.loadAssignments()

        courseApi.get_upcoming_course_deadlines(this.cID)
            .then(response => {
                this.deadlines = response
            })
    },
    methods: {
        loadAssignments () {
            assignment.get_course_assignments(this.cID)
                .then(response => { this.assignments = response })
        },
        showModal (ref) {
            this.$refs[ref].show()
        },
        handleConfirm (ref) {
            if (ref === 'createAssignmentRef') {
                this.loadAssignments()
            } else if (ref === 'editAssignmentRef') {
                // TODO: handle edit assignment
            }

            this.hideModal(ref)
        },
        hideModal (ref) {
            this.$refs[ref].hide()
        },
        customisePage () {
            this.$toasted.info('Wishlist: Customise page')
        },
        handleEdit () {
            this.$router.push({
                name: 'CourseEdit',
                params: {
                    cID: this.cID
                }
            })
        },
        assignmentRoute (cID, aID, name, journal) {
            if (this.$root.canViewAssignmentParticipants()) {
                return {
                    name: 'Assignment',
                    params: {
                        cID: cID,
                        aID: aID,
                        assignmentName: name
                    }
                }
            } else {
                var obj = {
                    name: 'Journal',
                    params: {
                        cID: cID,
                        aID: aID,
                        assignmentName: name
                    }
                }
                if (journal) {
                    obj.params.jID = journal.jID
                }

                return obj
            }
        },
        journalRoute (cID, aID, jID, name) {
            if (this.$root.canViewAssignmentParticipants()) {
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
            var counter = 0

            function compareDate (a, b) {
                return new Date(a.deadline.Date) - new Date(b.deadline.Date)
            }

            function compareMarkingsNeeded (a, b) {
                if (a.totalNeedsMarking > b.totalNeedsMarking) { return -1 }
                if (a.totalNeedsMarking < b.totalNeedsMarking) { return 1 }
                return 0
            }

            function filterTop () {
                return (++counter <= 5)
            }

            function filterNoEntries (deadline) {
                return deadline.totalNeedsMarking !== 0
            }

            if (this.selectedSortOption === 'sortDate') {
                return this.deadlines.slice().sort(compareDate).filter(filterTop)
            } else if (this.selectedSortOption === 'sortNeedsMarking') {
                return this.deadlines.slice().sort(compareMarkingsNeeded).filter(filterTop).filter(filterNoEntries)
            } else {
                return this.deadlines.slice().sort(compareDate).filter(filterTop)
            }
        }
    }
}
</script>
