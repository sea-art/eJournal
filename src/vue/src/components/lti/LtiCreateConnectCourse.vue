<template>
    <div>
        <div v-if="courses">
            <span class="multi-form">If you would like to create a course on eJournal please click the button below.</span>
            <b-row align-h="center">
                <b-button class="lti-button-option" @click="showModal('createCourseRef')">
                    <icon name="plus-square" scale="1.8"/>
                    <h2 class="lti-button-text">Create course</h2>
                </b-button>
            </b-row>

            <span class="multi-form">If you have already setup a course on eJournal, and would like to link the canvas
            course to this course. Please select the course below.</span>
            <b-row align-h="center">
                <b-button class="lti-button-option" @click="showModal('connectCourseRef')">
                    <icon name="link" scale="1.8"/>
                    <h2 class="lti-button-text">Couple course</h2>
                </b-button>
            </b-row>
        </div>

        <b-modal
            ref="createCourseRef"
            title="New Course"
            size="lg"
            hide-footer>
                <create-course @handleAction="handleCreation" :lti="lti"/>
        </b-modal>

        <b-modal
            ref="connectCourseRef"
            title="Connect Course"
            size="lg"
            hide-footer>
                <connect-course @handleAction="handleConnected" :lti="lti" :courses="courses"/>
        </b-modal>
    </div>
</template>

<script>
import createCourse from '@/components/course/CreateCourse.vue'
import connectCourse from '@/components/lti/ConnectCourse.vue'
import icon from 'vue-awesome/components/Icon'

export default {
    name: 'LtiCreateConnectCourse',
    props: ['lti', 'courses'],
    components: {
        'create-course': createCourse,
        'connect-course': connectCourse,
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
        handleConnected (cID) {
            this.hideModal('connectCourseRef')
            this.signal(['courseConnected', cID])
        }
    }
}
</script>
