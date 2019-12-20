<template>
    <div>
        <h2 class="theme-h2 multi-form">
            Configuring an assignment
        </h2>
        <span class="d-block mb-2">
            You came here from a learning management system through an unconfigured
            assignment. Select one of the options below to perform a one-time configuration.
        </span>
        <b-card class="no-hover">
            <b-button
                class="add-button big-button-text full-width"
                @click="showModal('createAssignmentRef')"
            >
                <icon
                    name="plus-square"
                    class="mr-3"
                    scale="1.8"
                />
                Create new assignment
            </b-button>
            <hr/>
            If you have not yet preconfigured this assignment on eJournal, click the button above
            to create a new assignment.
        </b-card>
        <b-card class="no-hover">
            <b-button
                v-b-modal="'lti-assignment-copy-modal'"
                class="add-button big-button-text full-width"
            >
                <icon
                    name="file"
                    class="mr-3"
                    scale="1.8"
                />
                Copy assignment
            </b-button>
            <assignment-copy-modal
                modalID="lti-assignment-copy-modal"
                :cID="page.cID"
                :lti="lti"
            />
            <hr/>
            If you want to create a new assignment that is identical to an assignment that you have
            already configured, click the button above to copy it. Existing journals are not copied
            and will remain accessible only from the original assignment.
        </b-card>
        <b-card
            v-if="linkableAssignments.some(linkable => linkable.assignments.length > 0)"
            class="no-hover"
        >
            <b-button
                class="change-button big-button-text full-width"
                @click="showModal('linkAssignmentRef')"
            >
                <icon
                    name="link"
                    class="mr-3"
                    scale="1.8"
                />
                Link to existing assignment
            </b-button>
            <hr/>
            If you have already configured an assignment on eJournal, you can link it to the assignment in
            your learning management system by clicking the button above. This allows students to continue
            working on their existing journals related to this assignment.
        </b-card>
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
    </div>
</template>

<script>
import createAssignment from '@/components/assignment/CreateAssignment.vue'
import linkAssignment from '@/components/lti/LinkAssignment.vue'
import assignmentCopyModal from '@/components/assignment/AssignmentCopyModal.vue'

export default {
    name: 'LtiCreateLinkAssignment',
    components: {
        createAssignment,
        linkAssignment,
        assignmentCopyModal,
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
