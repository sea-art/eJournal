<template>
    <div>
        <p class="lti-intro-text">You came here from canvas with an unknown
            user account. Do you want to create a new user on Logboek,
            or connect to an existing one?</p>
        <b-row align-h="center">
            <b-button class="lti-button-option" @click="showModal('createUserRef')">
                <h2 class="lti-button-text">Create new user</h2>
            </b-button>
        </b-row>
        <b-row  align-h="center">
            <b-button class="lti-button-option" @click="showModal('connectUserRef')">
                <h2 class="lti-button-text">Connect to existing user</h2>
            </b-button>
        </b-row>

        <b-modal
            ref="createUserRef"
            title="Create user"
            size="lg"
            hide-footer>
                <create-user @handleAction="handleIntegrated('createUserRef')" :lti="lti"/>
        </b-modal>

        <b-modal
            ref="connectUserRef"
            title="Connect user"
            size="lg"
            hide-footer>
                <connect-user @handleAction="handleIntegrated('connectUserRef')" :lti="lti"/>
        </b-modal>
    </div>
</template>

<script>
import createUser from '@/components/CreateUser.vue'
import connectUser from '@/components/ConnectUser.vue'

export default {
    name: 'LtiCreateConnectUser',
    props: ['lti'],
    components: {
        'create-user': createUser,
        'connect-user': connectUser
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
        handleIntegrated (ref) {
            this.hideModal(ref)
            this.signal(['userIntegrated'])
        }
    }
}
</script>
