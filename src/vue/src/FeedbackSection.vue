<template>
    <div class="feedback-wrapper">
        <div
            v-if="loggedIn"
            class="small-shadow feedback-button"
            @click="showModal('feedbackModal')">
            <icon name="comments"/>
            Feedback
        </div>

        <b-modal
            ref="feedbackModal"
            size="lg"
            title="Send technical feedback"
            hide-footer>
            <feedback-form @feedbackSent="hideModal('feedbackModal')"/>
        </b-modal>
    </div>
</template>

<script>
import icon from 'vue-awesome/components/Icon'
import Feedback from '@/components/assets/Feedback.vue'

import { mapGetters } from 'vuex'

export default {
    components: {
        icon,
        'feedback-form': Feedback
    },
    computed: {
        ...mapGetters({
            loggedIn: 'user/loggedIn',
            profileImg: 'user/profilePicture'
        })
    },
    methods: {
        showModal (ref) {
            this.$refs[ref].show()
        },
        hideModal (ref) {
            this.$refs[ref].hide()
        }
    }
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'
@import '~sass/modules/breakpoints.sass'

.feedback-wrapper
    display: absolute
    .feedback-button
        cursor: pointer
        padding: 2px 10px 2px 10px
        position: fixed
        bottom: 0px
        right: 50px
        background-color: $theme-medium-grey
        @include md-max
            float: right
            position: relative
        &:hover
            color: $theme-blue
</style>
