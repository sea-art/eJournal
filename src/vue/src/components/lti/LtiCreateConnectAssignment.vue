<template>
    <div>
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
            ref="createAssignmentRef"
            title="Create assignment"
            size="lg"
            hide-footer>
                <create-assignment @handleAction="handleCreated" :lti="lti" :page="page"/>
        </b-modal>

        <b-modal
            ref="connectAssignmentRef"
            title="Connect assignment"
            size="lg"
            hide-footer>
                <connect-assignment @handleAction="handleConnected" :lti="lti" :page="page"/>
        </b-modal>
    </div>
</template>

<script>
import createAssignment from '@/components/assignment/CreateAssignment.vue'
import connectAssignment from '@/components/lti/ConnectAssignment.vue'

export default {
    name: 'LtiCreateConnectAssignment',
    props: ['lti', 'page'],
    components: {
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
        handleCreated (aID) {
            this.hideModal('createAssignmentRef')
            this.signal(['assignmentIntegrated', aID])
        },
        handleConnected (aID) {
            this.hideModal('connectAssignmentRef')
            this.signal(['assignmentIntegrated', aID])
        }
    }
}
</script>
