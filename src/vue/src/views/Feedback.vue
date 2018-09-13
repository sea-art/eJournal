<template>
    <content-single-column>
        <bread-crumb>&nbsp;</bread-crumb>
        <b-card class="no-hover blue-border">
            <h2>Send the developers your feedback</h2>
            Hi! If you have any suggestions for improvements or found
            any issues/bugs please inform us and fill in the form below. Thank you!
        </b-card>
        <b-card class="no-hover blue-border">
        <h2 class='field-heading'>Topic:</h2>
                <b-input
                    class="theme-input multi-form"
                    v-model="topic"
                    type="text"
                    required
                />
            <h2 class='field-heading'>Type of feedback:</h2>
            <b-form-select
                class="theme-input multi-form"
                :options="types"
                required
                v-model="type"/>

            <h2 class='field-heading'>Feedback:</h2>
            <div class="multi-form">
                <text-editor
                    :id="'rich-text-editor'"
                    :givenContent="feedback.data"
                    @content-update="feedback.data = $event"
                />
            </div>

            <b-button class="add-button float-right mt-2" @click="sendFeedback">
                <icon name="paper-plane"/>
                Send
            </b-button>
        </b-card>
    </content-single-column>
</template>

<script>
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import textEditor from '@/components/assets/TextEditor.vue'
import icon from 'vue-awesome/components/Icon'
import feedback from '@/api/feedback'

export default {
    data () {
        return {
            topic: '',
            feedback: [],
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
        'bread-crumb': breadCrumb,
        'text-editor': textEditor,
        icon
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
                this.$toasted.error('yo')
                console.log('feedback: ' + this.feedback)
                console.log('event:' + this.$event)
                feedback.sendFeedback(this.topic, this.type, this.feedback, navigator.userAgent)
                    .then(response => { this.$toasted.success(response.data.description) })
                    .catch(error => { this.$toasted.error(error.response.data.description) })
            }
        }
    }

}
</script>
