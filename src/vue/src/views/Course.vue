<template>
    <content-columns>
        <bread-crumb
            slot="main-content-column"
            @eye-click="customisePage"
            @edit-click="handleEdit()"/>

        <div slot="main-content-column" v-for="a in assignments" :key="a.id">
            <b-link tag="b-button" :to="assignmentRoute(cID, a.id, a.journal)">
                <assignment-card :line1="a.name">
                    <progress-bar
                        v-if="a.journal && a.journal.stats"
                        :currentPoints="a.journal.stats.acquired_points"
                        :totalPoints="a.journal.stats.total_points"/>
                    <b-button v-if="$hasPermission('can_delete_assignment')" @click.prevent.stop="deleteAssignment(a.id)" class="delete-button float-right">
                        <icon name="trash"/>
                        Remove
                    </b-button>
                </assignment-card>
            </b-link>
        </div>

        <b-button v-if="$hasPermission('can_add_assignment')"
            slot="main-content-column"
            class="add-button grey-background full-width"
            @click="showModal('createAssignmentRef')">
            <icon name="plus"/>
            Create New Assignment
        </b-button>

        <h3 slot="right-content-column">To Do</h3>

        <!-- TODO Permission revision should be can_grade -->
        <b-card v-if="$hasPermission('can_view_assignment_participants')"
                class="no-hover"
                slot="right-content-column">
            <b-form-select v-model="selectedSortOption" :select-size="1">
                <option value="sortDate">Sort by date</option>
                <option value="sortNeedsMarking">Sort by marking needed</option>
            </b-form-select>
        </b-card>

        <div v-for="(d, i) in computedDeadlines" :key="i" slot="right-content-column">
            <b-link tag="b-button" :to="assignmentRoute(d.course.id, d.id, d.journal)">
                <todo-card :deadline="d"/>
            </b-link>
        </div>
        <b-modal
            slot="main-content-column"
            ref="createAssignmentRef"
            title="New Assignment"
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
import mainCard from '@/components/assets/MainCard.vue'
import icon from 'vue-awesome/components/Icon'
import createAssignment from '@/components/assignment/CreateAssignment.vue'

import assignmentAPI from '@/api/assignment'

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
            selectedSortOption: 'sortDate',
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
        'create-assignment': createAssignment,
        icon
    },
    created () {
        this.loadAssignments()
    },
    methods: {
        loadAssignments () {
            assignmentAPI.getAllFromCourse(this.cID)
                .then(assignments => { this.assignments = assignments })
                .catch(error => { this.$toasted.error(error.response.data.description) })

            assignmentAPI.getUpcoming(this.cID)
                .then(deadlines => { this.deadlines = deadlines })
                .catch(error => { this.$toasted.error(error.response.data.description) })
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
        assignmentRoute (cID, aID, jID) {
            var route = {
                params: {
                    cID: cID,
                    aID: aID
                }
            }

            // TODO Permission revision can_grade
            if (this.$hasPermission('can_view_assignment_participants', 'assignment', String(aID))) {
                route.name = 'Assignment'
            } else {
                route.name = 'Journal'
                route.params.jID = jID
            }

            return route
        },
        deleteAssignment (aID) {
            if (confirm('Are you sure you want to remove this assignment from this course?')) {
                assignmentAPI.delete(aID, this.cID)
                    .then(_ => {
                        this.$toasted.success('Removed assignment.')
                        this.loadAssignments()
                    })
                    .catch(error => { this.$toasted.error(error.response.data.description) })
            }
        }
    },
    computed: {
        computedDeadlines: function () {
            var counter = 0

            function compareDate (a, b) {
                if (!a.deadline) { return b.deadline }
                if (!b.deadline) { return a.deadline }
                return new Date(a.deadline.Date) - new Date(b.deadline.Date)
            }

            function compareMarkingNeeded (a, b) {
                if (a.stats.needs_marking > b.stats.needs_marking) { return -1 }
                if (a.stats.needs_marking < b.stats.needs_marking) { return 1 }
                return 0
            }

            function filterTop () {
                return ++counter <= 5
            }

            if (this.selectedSortOption === 'sortDate') {
                return this.deadlines.slice().sort(compareDate).filter(filterTop)
            } else if (this.selectedSortOption === 'sortNeedsMarking') {
                return this.deadlines.slice().sort(compareMarkingNeeded).filter(filterTop)
            } else {
                return this.deadlines.slice().sort(compareDate).filter(filterTop)
            }
        }
    }
}
</script>
