<template>
    <content-columns>
        <bread-crumb
            @eye-click="customisePage()"
            @edit-click="showModal('editCourseRef')"
            slot="main-content-column"
            :currentPage="'Courses'">
        </bread-crumb>

        <div v-for="c in courses" :key="c.id" slot="main-content-column">
            <b-link :to="{name: 'Course', params: {cID: c.id, courseName: c.name}}">
                <main-card
                    :line1="c.name"
                    :line2="c.startdate ? (c.startdate.substring(0, 4) + (c.enddate ? ' - ' + c.enddate.substring(0, 4) : '')) : ''"
                    :color="$root.getBorderClass(c.cID)">
                </main-card>
            </b-link>
        </div>
        <b-button v-if="$root.canAddCourse()"
            slot="main-content-column"
            class="add-button grey-background full-width"
            @click="showModal('createCourseRef')">
            <icon name="plus"/>
            Create New Course
        </b-button>

        <h3 slot="right-content-column">Upcoming</h3>
        <!-- TODO: This seems like an inappropriate permission check. Will have to be reconsidered in the rework. -->
        <b-card v-if="this.$root.canAddCourse()"
                class="no-hover"
                slot="right-content-column">
            <b-form-select v-model="selectedSortOption" :select-size="1">
                <option value="sortDate">Sort by date</option>
                <option value="sortNeedsMarking">Sort by marking needed</option>
            </b-form-select>
        </b-card>

        <div v-for="(d, i) in computedDeadlines" :key="i" slot="right-content-column">
            <b-link tag="b-button" :to="assignmentRoute(d.cID, d.aID, d.jID)">
                <todo-card
                    :date="d.deadline.Date"
                    :hours="d.deadline.Hours"
                    :minutes="d.deadline.Minutes"
                    :name="d.name"
                    :abbr="d.courseAbbr"
                    :totalNeedsMarking="d.totalNeedsMarking"
                    :class="$root.getBorderClass(d.cID)">
                </todo-card>
            </b-link>
        </div>

        <b-modal
            slot="main-content-column"
            ref="editCourseRef"
            title="Global Changes"
            size="lg"
            hide-footer>
                <edit-home @handleAction="handleConfirm('editCourseRef')"></edit-home>
        </b-modal>

        <b-modal
            slot="main-content-column"
            ref="createCourseRef"
            title="New Course"
            size="lg"
            hide-footer>
                <create-course @handleAction="handleConfirm('createCourseRef')"></create-course>
        </b-modal>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/columns/ContentColumns.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import mainCard from '@/components/assets/MainCard.vue'
import todoCard from '@/components/assets/TodoCard.vue'
import createCourse from '@/components/course/CreateCourse.vue'
import editHome from '@/components/home/EditHome.vue'

import auth from '@/api/auth'

import icon from 'vue-awesome/components/Icon'

export default {
    name: 'Home',
    data () {
        return {
            intituteName: 'Universiteit van Amsterdam (UvA)',
            courses: [],
            selectedSortOption: 'sortDate',
            deadlines: []
        }
    },
    components: {
        'content-columns': contentColumns,
        'bread-crumb': breadCrumb,
        'main-card': mainCard,
        'todo-card': todoCard,
        'create-course': createCourse,
        'edit-home': editHome,
        'icon': icon
    },
    created () {
        this.loadCourses()

        // assignmentApi.get_upcoming_deadlines()
        //     .then(response => {
        //         this.deadlines = response
        //     })
        //     .catch(_ => this.$toasted.error('Error while loading deadlines'))
    },
    methods: {
        loadCourses () {
            auth.get('courses').then(courses => { this.courses = courses })
        },
        deleteCourse (courseID, courseName) {
            if (confirm('Are you sure you want to delete ' + courseName + '?')) {
                // TODO: Implement delete this course ID after privy check
            }
        },
        showModal (ref) {
            this.$refs[ref].show()
        },
        handleConfirm (ref) {
            if (ref === 'createCourseRef') {
                this.loadCourses()
            } else if (ref === 'editCourseRef') {
                // TODO: Handle edit course
            }

            this.hideModal(ref)
        },
        hideModal (ref) {
            this.$refs[ref].hide()
        },
        customisePage () {
            this.$toasted.info('Wishlist: Customise page')
        },
        assignmentRoute (cID, aID, jID) {
            var route = {
                name: 'Assignment',
                params: {
                    cID: cID,
                    aID: aID
                }
            }

            if (jID) {
                route.params.jID = jID
            }

            return route
        }
    },
    computed: {
        computedDeadlines: function () {
            var counter = 0

            function compareDate (a, b) {
                return new Date(a.deadline.Date) - new Date(b.deadline.Date)
            }

            function compareMarkingNeeded (a, b) {
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
                return this.deadlines.slice().sort(compareMarkingNeeded).filter(filterTop).filter(filterNoEntries)
            } else {
                return this.deadlines.slice().sort(compareDate).filter(filterTop)
            }
        }
    }
}
</script>
