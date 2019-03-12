<template>
    <div class="feedback-wrapper">
        <div
            v-if="loggedIn"
            class="shadow feedback-button"
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
    position: absolute
    .feedback-button
        font-family: 'Roboto Condensed', sans-serif
        cursor: pointer
        padding: 2px 10px 2px 10px
        position: fixed
        bottom: 0px
        left: 50px
        background-color: white
        border-width: 2px 2px 0px 2px
        border-color: $theme-dark-grey
        border-radius: 5px 5px 0px 0px !important
        font-weight: bold
        svg
            fill: $theme-dark-blue
        @include md-max
            float: right
            position: relative
        &:hover
            background-color: $theme-dark-blue
            color: white
            svg
                fill: $theme-orange
</style>
