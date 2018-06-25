<template>
    <div slot="main-content-column">
        <p class="lti-intro-text">You came here from canvas with an unknown
            assignment. Do you want to create a new assignment on Logboek,
            or connect to an existing one?</p>
        <b-row align-h="center">
            <b-button class="lti-button-option" @click="showModal('createAssignmentRef')">
                <h2 class="lti-button-text">Create new assignment</h2>
            </b-button>
        </b-row>
        <b-row  align-h="center">
            <b-button class="lti-button-option" @click="showModal('connectAssignmentRef')">
                <h2 class="lti-button-text">Connect to existing <br/> assignment</h2>
            </b-button>
        </b-row>

        <b-modal
            slot="main-content-column"
            ref="createAssignmentRef"
            title="Create assignment"
            size="lg"
            hide-footer>
                <create-assignment @handleAction="handleConfirm('createAssignmentRef')" :lti="lti"/>
        </b-modal>

        <b-modal
            slot="main-content-column"
            ref="connectAssignmentRef"
            title="Connect assignment"
            size="lg"
            hide-footer>
                <connect-assignment @handleAction="handleConfirm('connectAssignmentRef')" :lti="lti"/>
        </b-modal>
    </div>
</template>

<script>
import breadCrumb from '@/components/BreadCrumb.vue'
import createAssignment from '@/components/CreateAssignment.vue'
import connectAssignment from '@/components/ConnectAssignment.vue'

export default {
    name: 'LtiCreateConnectAssignment',
    props: ['lti'],
    components: {
        'bread-crumb': breadCrumb,
        'create-assignment': createAssignment,
        'connect-assignment': connectAssignment
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
