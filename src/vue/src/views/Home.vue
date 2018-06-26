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
                    :line2="'From - To (years eg: 2017 - 2018)'"
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
        <div v-for="d in deadlines" :key="d.dID" slot="right-content-column">
            <b-link tag="b-button" :to="{name: 'Assignment', params: {cID: d.cIDs[0], aID: d.aIDs[0], dID: d.dID}}">
                <todo-card
                    :line0="d.datetime"
                    :line1="d.name"
                    :line2="d.courseAbbrs.join(', ')"
                    :color="$root.colors[d.cIDs[0] % $root.colors.length]">
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

export default {
    name: 'Home',
    data () {
        return {
            intituteName: 'Universiteit van Amsterdam (UvA)',
            courses: [],
            // TODO real deadlines with API, can a deadline be bound > 1 course and assignment?
            deadlines: [{
                name: 'Individueel logboek',
                cIDs: ['1', '2'],
                aIDs: ['1', '3'],
                courseAbbrs: ['WEDA', 'PALSIE8'],
                aID: '1',
                datetime: '8-6-2018 13:00'
            }]
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

        /* assignment.get_upcoming_deadlines()
           .then(response => { this.deadlines = response })
           .catch(_ => alert('Error while loading deadlines')) */
    },
    methods: {
        loadCourses () {
            course.get_user_courses()
                .then(response => { this.courses = response })
                .catch(_ => alert('Error while loading courses'))
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
            alert('Wishlist: Customise page')
        },
        canDeleteCourse () {
            return this.$root.permissions.can_delete_course
        }
    }
}
</script>
