<template>
    <content-columns>
        <bread-crumb slot="main-content-column" :currentPage="'Courses'" @edit-click="handleEdit()"/>

        <h2 slot="main-content-column">Input to be displayed</h2>
        <textarea slot="main-content-column" v-model="test" class="w-100" @input="injectContent($refs['iframe1'])"/>

        <h2 slot="main-content-column">V-html</h2>
        <div v-html="test" slot="main-content-column"/>

        <h2 slot="main-content-column">Sandboxed iframe</h2>
        <iframe slot="main-content-column" ref="iframe1" @load="test2" id="iframe1" sandbox="allow-same-origin" frameBorder="0" marginwidth="0" marginheight="0" class="w-100" scrolling="no"/>

        <h2 slot="main-content-column">V-html-sanitized</h2>
        <div v-html="$sanitize(test)" slot="main-content-column"/>

        <div v-for="c in courses" :key="c.id" slot="main-content-column">
            <b-link :to="{ name: 'Course', params: { cID: c.id, courseName: c.name } }">
                <main-card
                    :line1="c.name"
                    :line2="c.startdate ? (c.startdate.substring(0, 4) + (c.enddate ? ' - ' + c.enddate.substring(0, 4) : '')) : ''"
                    :color="$root.getBorderClass(c.id)" />
            </b-link>
        </div>
        <b-button v-if="$hasPermission('can_add_course')"
            slot="main-content-column"
            class="add-button grey-background full-width"
            @click="showModal('createCourseRef')">
            <icon name="plus"/>
            Create New Course
        </b-button>

        <h3 slot="right-content-column">To Do</h3>
        <deadline-deck slot="right-content-column" :deadlines="deadlines"/>

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
import deadlineDeck from '@/components/assets/DeadlineDeck.vue'

import courseAPI from '@/api/course'
import assignmentAPI from '@/api/assignment'

import icon from 'vue-awesome/components/Icon'

export default {
    name: 'Home',
    data () {
        return {
            test: '<button onclick="alert(\'hoi\')">Click me</button>',
            intituteName: 'Universiteit van Amsterdam (UvA)',
            courses: [],
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
        'deadline-deck': deadlineDeck,
        icon
    },
    created () {
        this.loadCourses()

        assignmentAPI.getUpcoming()
            .then(deadlines => { this.deadlines = deadlines })
    },
    mounted () {
        this.test1()
    },
    methods: {
        injectContent (obj) {
            var doc = obj.contentWindow.document
            doc.open()
            doc.write(this.test)
            doc.close()
        },
        test1 () {
            console.log(this.$refs['iframe1'])
            this.$refs['iframe1'].height = 21
        },
        test2 (e) {
            console.log(e)
            console.log('2')
        },
        loadCourses () {
            courseAPI.getUserEnrolled()
                .then(courses => { this.courses = courses })
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
        }
    }
}
</script>
