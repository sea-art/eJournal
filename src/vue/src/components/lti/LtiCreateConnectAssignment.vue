<template>
    <div>
        <p class="lti-intro-text">You came here from a learning environment with an unknown
            assignment. Do you want to create a new assignment on Logboek,
            or link to an existing one?</p>
        <b-row align-h="center" class="multi-form">
            <b-button class="lti-button-option" @click="showModal('createAssignmentRef')">
                <icon name="plus-square" scale="1.8"/>
                <h2 class="lti-button-text">Create new assignment</h2>
            </b-button>
        </b-row>
        <b-row  align-h="center">
            <b-button class="lti-button-option" @click="showModal('linkAssignmentRef')">
                <icon name="link" scale="1.8"/>
                <h2 class="lti-button-text">Link to existing <br/> assignment</h2>
            </b-button>
        </b-row>

        <b-modal
            ref="createAssignmentRef"
            title="New Assignment"
            size="lg"
            hide-footer>
                <create-assignment @handleAction="handleCreated" :lti="lti" :page="page"/>
        </b-modal>

        <b-modal
            ref="linkAssignmentRef"
            title="Link Assignment"
            size="lg"
            hide-footer>
                <connect-assignment @handleAction="handleConnected" :lti="lti" :page="page"/>
        </b-modal>
    </div>
</template>

<script>
import createAssignment from '@/components/assignment/CreateAssignment.vue'
import connectAssignment from '@/components/lti/ConnectAssignment.vue'
import icon from 'vue-awesome/components/Icon'

export default {
    name: 'LtiCreateConnectAssignment',
    props: ['lti', 'page'],
    components: {
        'create-assignment': createAssignment,
        'connect-assignment': connectAssignment,
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
        handleCreated (aID) {
            this.hideModal('createAssignmentRef')
            this.signal(['assignmentCreated', aID])
        },
        handleConnected (aID) {
            this.hideModal('linkAssignmentRef')
            this.signal(['assignmentIntegrated', aID])
        }
    }
}
</script>
