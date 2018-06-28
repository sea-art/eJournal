<template>
    <content-columns>
        <bread-crumb
            @eye-click="customisePage()"
            @edit-click="showModal('editCourseRef')"
            slot="main-content-column"
            :currentPage="'Courses'">
        </bread-crumb>
        <div v-for="c in courses" :key="c.cID" slot="main-content-column">
            <b-link :to="{name: 'Course', params: {cID: c.cID, courseName: c.name}}">
                <main-card
                    :line1="c.name"
                    :line2="c.startdate.substring(0, 4) + '-' + c.enddate.substring(0, 4)"
                    :color="$root.colors[c.cID % $root.colors.length]">
                </main-card>
            </b-link>
        </div>
        <main-card
            v-if="this.$root.canAddCourse()"
            slot="main-content-column"
            class="hover"
            @click.native="showModal('createCourseRef')"
            :line1="'+ Add course'"/>

        <h3 slot="right-content-column">Upcoming</h3>

        <div v-for="(d, i) in computedDeadlines" :key="i" slot="right-content-column">
            <b-link tag="b-button" :to="journalRoute(d.cID, d.aID, d.jID, d.name)">
                <todo-card
                    :date="d.deadline.Date"
                    :hours="d.deadline.Hours"
                    :minutes="d.deadline.Minutes"
                    :name="d.name"
                    :abbr="d.courseAbbr"
                    :totalNeedsMarking="needsMarkingStats[i]"
                    :color="$root.colors[d.cID % $root.colors.length]">
                </todo-card>
            </b-link>
        </div>

        <b-modal
            slot="main-content-column"
            ref="editCourseRef"
            title="Global changes"
            size="lg"
            hide-footer>
                <edit-home @handleAction="handleConfirm('editCourseRef')"></edit-home>
        </b-modal>

        <b-modal
            slot="main-content-column"
            ref="createCourseRef"
            title="Create course"
            size="lg"
            hide-footer>
                <create-course @handleAction="handleConfirm('createCourseRef')"></create-course>
        </b-modal>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
import mainCard from '@/components/MainCard.vue'
import todoCard from '@/components/TodoCard.vue'
import createCourse from '@/components/CreateCourse.vue'
import editHome from '@/components/EditHome.vue'
import course from '@/api/course'
import assignmentApi from '@/api/assignment.js'
import journalApi from '@/api/journal.js'

export default {
    name: 'Home',
    data () {
        return {
            intituteName: 'Universiteit van Amsterdam (UvA)',
            courses: [],
            deadlines: [],
            needsMarkingStats: []
        }
    },
    components: {
        'content-columns': contentColumns,
        'bread-crumb': breadCrumb,
        'main-card': mainCard,
        'todo-card': todoCard,
        'create-course': createCourse,
        'edit-home': editHome
    },
    created () {
        this.loadCourses()

        assignmentApi.get_upcoming_deadlines()
            .then(response => {
                this.deadlines = response
            })
            .catch(_ => alert('Error while loading deadlines'))
    },
    methods: {
        loadCourses () {
            course.get_user_courses()
                .then(response => { this.courses = response })
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
                // TODO: Handle edit assignment
            }

            this.hideModal(ref)
        },
        hideModal (ref) {
            this.$refs[ref].hide()
        },
        customisePage () {
            this.$toasted.info('Wishlist: Customise page')
        },
        addMarkingList (aID) {
            journalApi.get_assignment_journals(aID)
                .then(response => {
                    this.needsMarkingStats.push(response.stats.needsMarking)
                })
                .catch(_ => alert('Error while loading journals'))
        },
        journalRoute (cID, aID, jID, name) {
            if (this.$root.canAddCourse()) {
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
            var count = 0
            var topList

            function compareDate (a, b) {
                return new Date(a.deadline.Date) - new Date(b.deadline.Date)
            }

            function filterTop () {
                if (++count <= 5) {
                    return true
                } else {
                    return false
                }
            }

            topList = this.deadlines.slice().sort(compareDate).filter(filterTop)

            if (this.$root.canAddCourse()) {
                for (var i = 0; i < topList.length; i++) {
                    this.addMarkingList(topList[i].aID)
                }
            }

            return topList
        }
    }
}
</script>
