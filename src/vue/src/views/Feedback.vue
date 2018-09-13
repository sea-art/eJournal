<template>
    <content-single-column>
        <bread-crumb>&nbsp;</bread-crumb>
        <b-card class="no-hover blue-border">
            <b-form-group label="Topic:">
                <b-input
                    class="theme-input multi-form"
                    v-model="topic"
                    type="text"
                    required
                />
            </b-form-group>
            <b-form-group label="Type of feedback:">
                <b-form-select
                    class="theme-input multi-form"
                    :options="types"
                    required
                    v-model="type"/>
            </b-form-group>

            <b-form-group label="Feedback:">
                <b-form-textarea
                    class="theme-input multi-form"
                    v-model="feedback"
                    :rows="4"
                    :max-rows="10"
                    required
                />
            </b-form-group>
            <b-button @click="sendFeedback" class="add-button float-right">
                <icon name="save"/>
                Send
            </b-button>
        </b-card>
    </content-single-column>
</template>

<script>
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'

import feedback from '@/api/feedback'

export default {
    data () {
        return {
            topic: '',
            feedback: '',
            type: null,
            types: [
                {text: 'Select one', value: null},
                'Issue/Bug', 'Suggestion', 'Other'
            ]
        }
    },
    name: 'Feedback',
    components: {
        'content-single-column': contentSingleColumn,
        'bread-crumb': breadCrumb
    },
    methods: {
        sendFeedback () {
            if (this.topic === '') {
                this.$toasted.error('Topic required')
            } else if (this.type == null) {
                this.$toasted.error('Choose a feedback type')
            } else if (this.body === '') {
                this.$toasted.error('Feedback required')
            } else {
                feedback.sendFeedback(this.topic, this.type, this.feedback, navigator.userAgent)
                    .then(response => { this.$toasted.success(response.data.description) })
                    .catch(error => { this.$toasted.error(error.response.data.description) })
            }
        }
    }

}
</script>
