<template>
    <div>
        <b-input-group class="multi-form">
            <b-input readonly class="theme-input" :value="$store.getters['user/email']" type="text"/>
            <b-input-group-text slot="append" class="theme-input input-append-icon round-border">
                <icon
                    v-if="!$store.getters['user/verifiedEmail']"
                    name="info"
                    v-b-tooltip.hover
                    :title="(showEmailValidationInput) ? 'Enter the email verification token below.' : 'Click to verify your email!'"
                    @click.native="requestEmailVerification"
                    class="crossed-icon"
                />
                <icon
                    v-if="$store.getters['user/verifiedEmail']"
                    name="check"
                    v-b-tooltip.hover
                    title="Your email is verified!"
                    class="checked-icon"
                />
            </b-input-group-text>
        </b-input-group>

        <b-input-group v-if="!$store.getters['user/verifiedEmail'] && showEmailValidationInput" class="multi-form">
            <b-input
            class="theme-input"
                v-b-tooltip.hover
                :title="(emailVerificationTokenMessage) ? emailVerificationTokenMessage : 'Enter your token'"
                required
                v-model="emailVerificationToken"
                placeholder="Enter the email verification token."
            />
            <b-input-group-text slot="append" class="theme-input input-append-icon round-border">
                <icon
                    name="paper-plane" class="validate-icon"
                    v-b-tooltip.hover title="Validate verification code."
                    @click.native="verifyEmail"
                />
            </b-input-group-text>
        </b-input-group>
    </div>
</template>

<script>
import userAPI from '@/api/user'
import icon from 'vue-awesome/components/Icon'

export default {
    components: {
        icon
    },
    data () {
        return {
            showEmailValidationInput: false,
            emailVerificationToken: null,
            emailVerificationTokenMessage: null
        }
    },
    methods: {
        requestEmailVerification () {
            if (!this.showEmailValidationInput) {
                userAPI.requestEmailVerification({responseSuccessToast: true})
                    .then(() => { this.showEmailValidationInput = true })
            }
        },
        verifyEmail () {
            userAPI.verifyEmail(this.$store.getters['user/username'], this.emailVerificationToken, {responseSuccessToast: true})
                .then(() => {
                    this.$store.commit('user/EMAIL_VERIFIED')
                    this.showEmailValidationInput = false
                })
                .catch(() => { this.emailVerificationTokenMessage = 'Invalid token' })
        }
    }
}
</script>
