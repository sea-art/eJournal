<template>
    <div v-if="courses">
        <h2 class="multi-form">Configuring a Course</h2>
        <span class="d-block mb-2">
            You came here from a learning environment through an unconfigured
            course. Do you want to create a new course on eJournal,
            or link it to an existing one?
        </span>
        <b-row>
            <b-col md="6">
                <b-card class="no-hover full-height">
                    <b-button class="add-button big-button-text full-width" @click="showModal('createCourseRef')">
                        <icon name="plus-square" class="mr-3" scale="1.8"/>
                        Create new<br/>course
                    </b-button>
                    <hr/>
                    If you have not yet preconfigured this course on eJournal, click the button above
                    to create a new course. This will be linked to your learning environment, allowing for automatic
                    grade passback.
                </b-card>
            </b-col>
            <b-col md="6">
                <b-card class="no-hover full-height">
                    <b-button class="change-button big-button-text full-width" @click="showModal('linkCourseRef')">
                        <icon name="link" class="mr-3" scale="1.8"/>
                        Link to existing<br/>course
                    </b-button>
                    <hr/>
                    If you have already set up a course on eJournal, you can link it to the course in
                    your learning environment by clicking the button above.
                </b-card>
            </b-col>

            <b-modal
                ref="createCourseRef"
                title="New Course"
                size="lg"
                hide-footer>
                    <create-course @handleAction="handleCreation" :lti="lti"/>
            </b-modal>

            <b-modal
                ref="linkCourseRef"
                title="Link Course"
                size="lg"
                hide-footer>
                    <link-course @handleAction="handleLinked" :lti="lti" :courses="courses"/>
            </b-modal>
        </b-row>
    </div>
</template>

<script>
import createCourse from '@/components/course/CreateCourse.vue'
import linkCourse from '@/components/lti/LinkCourse.vue'
import icon from 'vue-awesome/components/Icon'

export default {
    name: 'LtiCreateLinkCourse',
    props: ['lti', 'courses'],
    components: {
        'create-course': createCourse,
        'link-course': linkCourse,
        icon
    },
    methods: {
        signal (msg) {
            this.$emit('handleAction', msg)
        },
        showModal (ref) {
            this.$refs[ref].show()
        },
        hideModal (ref) {
            this.$refs[ref].hide()
        },
        handleCreation (cID) {
            this.hideModal('createCourseRef')
            this.signal(['courseCreated', cID])
        },
        handleLinked (cID) {
            this.hideModal('linkCourseRef')
            this.signal(['courseLinked', cID])
        }
    }
}
</script>
