<template>
    <div>
        <p class="lti-intro-text">You came here from canvas with an unknown
            assignment. Click on the button to create a new assignment on
            Logboek.</p>
        <b-row align-h="center">
            <b-button class="lti-button-option" @click="showModal('createAssignmentRef')">
                <icon name="plus-square" scale="1.8"/>
                <h2 class="lti-button-text">Create new assignment</h2>
            </b-button>
        </b-row>

        <b-modal
            ref="createAssignmentRef"
            title="New Assignment"
            size="lg"
            hide-footer>
                <create-assignment @handleAction="handleCreated" :lti="lti" :page="page"/>
        </b-modal>
    </div>
</template>

<script>
import createAssignment from '@/components/assignment/CreateAssignment.vue'
import icon from 'vue-awesome/components/Icon'

export default {
    name: 'LtiCreateAssignment',
    props: ['lti', 'page'],
    components: {
        'create-assignment': createAssignment,
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
        }
    },
    mounted () {
        this.showModal('createAssignmentRef')
    }
}
</script>
