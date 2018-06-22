<template>
    <div slot="main-content-column">
        <p class="lti-intro-text">You came here from canvas with an unknown
            assignment. Click on the button to create a new assignment on
            Logboek.</p>
        <b-row align-h="center">
            <b-button class="lti-button-option" @click="showModal('createAssignmentRef')">
                <h2 class="lti-button-text">Create new assignment</h2>
            </b-button>
        </b-row>

        <b-modal
            slot="main-content-column"
            ref="createAssignmentRef"
            title="Create assignment"
            size="lg"
            hide-footer>
                <create-assignment @handleAction="handleConfirm('createAssignmentRef')"/>
        </b-modal>
    </div>
</template>

<script>
import breadCrumb from '@/components/BreadCrumb.vue'
import createAssignment from '@/components/CreateAssignment.vue'

export default {
    name: 'LtiCreateConnect',
    components: {
        'bread-crumb': breadCrumb,
        'create-assignment': createAssignment
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
            this.signal('assignementCreated')
        }
    },
    mounted () {
        this.showModal('createAssignmentRef')
    }
}
</script>
