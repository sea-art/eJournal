<template>
    <content-single-column class="small-error">
        <h1 class="mb-2">
            <span>
                Error {{ code }}: <span class="text-grey">{{ reasonPhrase }}</span>
            </span>
        </h1>
        <b-card
            v-if="description !== null"
            class="no-hover"
        >
            <b>Message:</b>
            {{ description }}
        </b-card>
        <b-card
            v-else
            class="no-hover"
        >
            We are sorry, but an unknown error has brought you here.
        </b-card>
        <sentry-feedback-form v-if="sentryLastEventID !== null"/>
        <b-button
            v-else
            :to="{name: 'Home'}"
        >
            <icon name="home"/>
            Home
        </b-button>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import sentryFeedbackForm from '@/components/sentry/SentryFeedbackForm.vue'
import { mapGetters } from 'vuex'

export default {
    name: 'ErrorPage',
    components: {
        sentryFeedbackForm,
        contentSingleColumn,
    },
    props: {
        code: {
            default: '520',
        },
        reasonPhrase: {
            default: 'Unknown Error',
        },
        description: {
            default: null,
        },
    },
    computed: {
        ...mapGetters({
            sentryLastEventID: 'sentry/lastEvenID',
        }),
    },
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'

.error-content
    padding: 40px

.description-container
    padding: 20px 0px


.small-error .offset-xl-3
    max-width: 600px
    margin-left: calc(50% - 300px)!important
</style>
