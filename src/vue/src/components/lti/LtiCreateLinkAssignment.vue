<template>
    <div>
        <h2 class="multi-form">Configuring an assignment</h2>
        <span class="d-block mb-2">
            You came here from a learning environment through an unconfigured
            assignment. Do you want to create a new assignment on eJournal,
            or link it to an existing one?
        </span>
        <b-row>
            <b-col md="6">
                <b-card class="no-hover full-height">
                    <b-button class="add-button big-button-text full-width" @click="showModal('createAssignmentRef')">
                        <icon name="plus-square" class="mr-3" scale="1.8"/>
                        Create new<br/>assignment
                    </b-button>
                    <hr/>
                    If you have not yet preconfigured this assignment on eJournal, click the button above
                    to create a new assignment. This will be linked to your learning environment, allowing for automatic
                    grade passback.
                </b-card>
            </b-col>
            <b-col md="6">
                <b-card class="no-hover full-height">
                    <b-button class="change-button big-button-text full-width" @click="showModal('linkAssignmentRef')">
                        <icon name="link" class="mr-3" scale="1.8"/>
                        Link to existing<br/>assignment
                    </b-button>
                    <hr/>
                    If you have already set up an assignment on eJournal, you can link it to the assignment in
                    your learning environment by clicking the button above.
                </b-card>
            </b-col>

            <b-modal
                ref="linkAssignmentRef"
                title="Link to existing assignment"
                size="lg"
                hide-footer>
                    <link-assignment @handleAction="handleLinked" :lti="lti" :page="page"/>
            </b-modal>
            <b-modal
                ref="createAssignmentRef"
                title="Create new assignment"
                size="lg"
                hide-footer>
                    <create-assignment @handleAction="handleCreated" :lti="lti" :page="page"/>
            </b-modal>
        </b-row>
    </div>
</template>

<script>
import createAssignment from '@/components/assignment/CreateAssignment.vue'
import linkAssignment from '@/components/lti/LinkAssignment.vue'
import icon from 'vue-awesome/components/Icon'

export default {
    name: 'LtiCreateLinkAssignment',
    props: ['lti', 'page'],
    components: {
        'create-assignment': createAssignment,
        'link-assignment': linkAssignment,
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
        handleLinked (aID) {
            this.hideModal('linkAssignmentRef')
            this.signal(['assignmentIntegrated', aID])
        }
    }
}
</script>
