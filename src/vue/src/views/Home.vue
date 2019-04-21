<template>
    <content-columns>
        <bread-crumb
            slot="main-content-column"
            :currentPage="'Courses'"
            @edit-click="handleEdit()"
        />

        <div
            v-for="c in courses"
            slot="main-content-column"
            :key="c.id"
        >
            <b-link :to="{ name: 'Course', params: { cID: c.id, courseName: c.name } }">
                <main-card
                    :line1="c.name"
                    :line2="c.startdate ? (c.startdate.substring(0, 4) +
                        (c.enddate ? ` - ${c.enddate.substring(0, 4)}` : '')) : ''"
                    :color="$root.getBorderClass(c.id)"
                />
            </b-link>
        </div>
        <b-button
            v-if="$hasPermission('can_add_course')"
            slot="main-content-column"
            class="add-button"
            @click="showModal('createCourseRef')"
        >
            <icon name="plus"/>
            Create New Course
        </b-button>

        <h3 slot="right-content-column">
            To Do
        </h3>
        <deadline-deck
            slot="right-content-column"
            :deadlines="deadlines"
        />

        <b-modal
            slot="main-content-column"
            ref="editCourseRef"
            title="Global Changes"
            size="lg"
            hideFooter
        >
            <edit-home @handleAction="handleConfirm('editCourseRef')"/>
        </b-modal>

        <b-modal
            slot="main-content-column"
            ref="createCourseRef"
            title="New Course"
            size="lg"
            hideFooter
        >
            <create-course @handleAction="handleConfirm('createCourseRef')"/>
        </b-modal>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/columns/ContentColumns.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import mainCard from '@/components/assets/MainCard.vue'
import createCourse from '@/components/course/CreateCourse.vue'
import editHome from '@/components/home/EditHome.vue'
import deadlineDeck from '@/components/assets/DeadlineDeck.vue'

import courseAPI from '@/api/course.js'
import assignmentAPI from '@/api/assignment.js'

export default {
    name: 'Home',
    components: {
        contentColumns,
        breadCrumb,
        mainCard,
        createCourse,
        editHome,
        deadlineDeck,
    },
    data () {
        return {
            intituteName: 'Universiteit van Amsterdam (UvA)',
            courses: [],
            deadlines: [],
        }
    },
    created () {
        this.loadCourses()

        assignmentAPI.getUpcoming()
            .then((deadlines) => { this.deadlines = deadlines })
    },
    methods: {
        loadCourses () {
            courseAPI.getUserEnrolled()
                .then((courses) => { this.courses = courses })
        },
        showModal (ref) {
            this.$refs[ref].show()
        },
        handleConfirm (ref) {
            if (ref === 'createCourseRef') {
                this.loadCourses()
            }

            this.hideModal(ref)
        },
        handleEdit () {
            // TODO: Open EditHome
        },
        hideModal (ref) {
            this.$refs[ref].hide()
        },
    },
}
</script>
