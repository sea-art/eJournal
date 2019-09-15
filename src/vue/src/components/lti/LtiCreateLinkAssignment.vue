<template>
    <div>
        <h2 class="multi-form">
            Configuring an assignment
        </h2>
        <span class="d-block mb-2">
            You came here from a learning management system through an unconfigured
            assignment. Do you want to create a new assignment on eJournal,
            or link it to an existing one?
        </span>
        <b-row>
            <b-col md="6">
                <b-card class="no-hover full-height">
                    <b-button
                        class="add-button big-button-text full-width"
                        @click="showModal('createAssignmentRef')"
                    >
                        <icon
                            name="plus-square"
                            class="mr-3"
                            scale="1.8"
                        />
                        Create new<br/>assignment
                    </b-button>
                    <hr/>
                    If you have not yet preconfigured this assignment on eJournal, click the button above
                    to create a new assignment. This will be linked to your learning environment, allowing for automatic
                    grade passback. Also choose this option if you wish to copy the assignment structure of an existing
                    assignment, but want students to start with a new journal.
                </b-card>
            </b-col>
            <b-col md="6">
                <b-card class="no-hover full-height">
                    <b-button
                        class="change-button big-button-text full-width"
                        @click="showModal('linkAssignmentRef')"
                    >
                        <icon
                            name="link"
                            class="mr-3"
                            scale="1.8"
                        />
                        Link to existing<br/>assignment
                    </b-button>
                    <hr/>
                    If you have already set up an assignment on eJournal, you can link it to the assignment in
                    your learning management system by clicking the button above. This allows students to continue
                    working on their existing journals related to this assignment.
                </b-card>
            </b-col>

            <b-modal
                ref="linkAssignmentRef"
                title="Link to existing assignment"
                size="lg"
                hideFooter
            >
                <link-assignment
                    :lti="lti"
                    :page="page"
                    :linkableAssignments="linkableAssignments"
                    @handleAction="handleLinked"
                />
            </b-modal>
            <b-modal
                ref="createAssignmentRef"
                title="Create new assignment"
                size="lg"
                hideFooter
            >
                <create-assignment
                    :lti="lti"
                    :page="page"
                    @handleAction="handleCreated"
                />
            </b-modal>
        </b-row>
    </div>
</template>

<script>
import createAssignment from '@/components/assignment/CreateAssignment.vue'
import linkAssignment from '@/components/lti/LinkAssignment.vue'

export default {
    name: 'LtiCreateLinkAssignment',
    components: {
        createAssignment,
        linkAssignment,
    },
    props: ['lti', 'page', 'linkableAssignments'],
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
        },
    },
}
</script>
