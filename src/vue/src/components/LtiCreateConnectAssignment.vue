<template>
    <div slot="main-content-column">
        <bread-crumb
            :currentPage="'Assignment Integration'">
        </bread-crumb>
            <p class="intro-text">You came here from canvas with an unknown
                assignment. Do you want to create a new assignment on Logboek,
                or connect to an existing one?</p>
        <b-row align-h="center">
            <b-button class="button-option" @click="showModal('createAssignmentRef')">
                <h2 class="button-text">Create new assignment</h2>
            </b-button>
        </b-row>
        <b-row  align-h="center">
            <b-button class="button-option" @click="showModal('connectAssignmentRef')">
                <h2 class="button-text">Connect to existing assignment</h2>
            </b-button>
        </b-row>

        <b-modal
            slot="main-content-column"
            ref="createAssignmentRef"
            title="Create course"
            size="lg"
            hide-footer>
                <create-assignment @handleAction="handleConfirm('createCourseRef')"></create-assignment>
        </b-modal>

        <!-- <b-modal
            slot="main-content-column"
            ref="connectAssignmentRef"
            title="Connect Course"
            size="lg"
            hide-footer>
                <connect-assignment @handleAction="handleConfirm('connectAssignmentRef')"></connect-assignment>
        </b-modal> -->
    </div>
</template>

<script>
import breadCrumb from '@/components/BreadCrumb.vue'
import createAssignment from '@/components/CreateAssignment.vue'
// import connectAssignment from '@/components/ConnectAssignment.vue'

export default {
    name: 'LtiCreateConnect',
    components: {
        'bread-crumb': breadCrumb,
        'create-assignment': createAssignment,
        // 'connect-assignment': connectAssignment
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
            this.signal('assignementIntegrated')
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
