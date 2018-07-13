<template>
    <div>
        <p class="lti-intro-text">You came here from canvas with an unknown
            course. Do you want to create a new course on Logboek,
            or connect to an existing one?</p>
        <b-row align-h="center">
            <b-button class="lti-button-option" @click="showModal('createCourseRef')">
                <h2 class="lti-button-text">Create new course</h2>
            </b-button>
        </b-row>
        <b-row  align-h="center">
            <b-button class="lti-button-option" @click="showModal('connectCourseRef')">
                <h2 class="lti-button-text">Connect to existing course</h2>
            </b-button>
        </b-row>

        <b-modal
            ref="createCourseRef"
            title="Create course"
            size="lg"
            hide-footer>
                <create-course @handleAction="handleCreation" :lti="lti"/>
        </b-modal>

        <b-modal
            ref="connectCourseRef"
            title="Connect course"
            size="lg"
            hide-footer>
                <connect-course @handleAction="handleConnected" :lti="lti"/>
        </b-modal>
    </div>
</template>

<script>
import createCourse from '@/components/course/CreateCourse.vue'
import connectCourse from '@/components/lti/ConnectCourse.vue'

export default {
    name: 'LtiCreateConnectCourse',
    props: ['lti'],
    components: {
        'create-course': createCourse,
        'connect-course': connectCourse
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
