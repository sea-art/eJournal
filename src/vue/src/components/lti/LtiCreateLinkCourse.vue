<template>
    <div>
        <div v-if="courses">
            <span class="multi-form">If you would like to create a course on eJournal please click the button below.</span><br/>
            <b-row align-h="center">
                <b-button class="lti-button-option" @click="showModal('createCourseRef')">
                    <icon name="plus-square" scale="1.8"/>
                    <h2 class="lti-button-text">Create course</h2>
                </b-button>
            </b-row>
            <br/><span class="multi-form">If you would like to link an existing course on eJournal to the learning environment please
            click the button below.</span><br/>
            <b-row align-h="center">
                <b-button class="lti-button-option" @click="showModal('linkCourseRef')">
                    <icon name="link" scale="1.8"/>
                    <h2 class="lti-button-text">Link course</h2>
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
            ref="linkCourseRef"
            title="Link Course"
            size="lg"
            hide-footer>
                <link-course @handleAction="handleLinked" :lti="lti" :courses="courses"/>
        </b-modal>
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
