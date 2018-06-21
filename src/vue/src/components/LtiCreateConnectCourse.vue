<template>
    <div slot="main-content-column">
        <bread-crumb
            :currentPage="'Course Integration'">
        </bread-crumb>
            <p class="intro-text">You came here from canvas with an unknown
                course. Do you want to create a new course on Logboek,
                or connect to an existing one?</p>
        <b-row align-h="center">
            <b-button class="button-option" @click="showModal('createCourseRef')">
                <h2 class="button-text">Create new course</h2>
            </b-button>
        </b-row>
        <b-row  align-h="center">
            <b-button class="button-option" @click="showModal('connectCourseRef')">
                <h2 class="button-text">Connect to existing course</h2>
            </b-button>
        </b-row>

        <b-modal
            slot="main-content-column"
            ref="createCourseRef"
            title="Create course"
            size="lg"
            hide-footer>
                <create-course @handleAction="handleConfirm('createCourseRef')"></create-course>
        </b-modal>

        <b-modal
            slot="main-content-column"
            ref="connectCourseRef"
            title="Connect Course"
            size="lg"
            hide-footer>
                <connect-course @handleAction="handleConfirm('connectCourseRef')"></connect-course>
        </b-modal>
    </div>
</template>

<script>
import breadCrumb from '@/components/BreadCrumb.vue'
import createCourse from '@/components/CreateCourse.vue'
// import connectCourse from '@/components/ConnectCourse.vue'

export default {
    name: 'LtiCreateConnect',
    components: {
        'bread-crumb': breadCrumb,
        'create-course': createCourse,
        // 'connect-course': connectCourse
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
        handleConfirm (ref) {
            this.hideModal(ref)
            this.signal('courseIntegrated')
        }
    }
}
</script>

<style>
.button-option {
    width: 275px;
    height: 100px;
    margin-top: 20px;
}

.button-text {
    font-size: 20px;
    text-align: center;
}

.intro-text {
    margin-left: 15px;
    margin-right: 15px;
}
</style>
