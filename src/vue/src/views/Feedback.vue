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
            <b-form-textarea
               class="theme-input multi-form"
               v-model="feedback"
               :rows="4"
               :max-rows="10"
               required
            />
            <h2 class='field-heading'>Attachments:</h2>
            <b-row>
                <b-col>
                    <b-form-file
                        v-model="files"
                        :state="Boolean(files)"
                        class="fileinput"
                        multiple
                        ref="fileinput"
                        @change="filesHandler"
                        placeholder="Choose a file...">
                    </b-form-file>
                </b-col>
                <b-col>
                    <b-button class="add-button float-right mt-2" @click="sendFeedback">
                        <icon name="paper-plane"/>
                        Send
                    </b-button>
                </b-col>
            </b-row>
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
            feedback: '',
            type: null,
            types: [
                {text: 'Select one', value: null},
                'Issue/Bug', 'Suggestion', 'Other'
            ],
            files: null
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
        filesHandler (e) {
            let files = e.target.files
            if (files.length < 1) { return }

            var uploadSize = 0
            for (var i = 0; i < files.length; i++) {
                uploadSize += files[i].size
                if (uploadSize > this.$root.maxEmailFileSizeBytes) {
                    this.$toasted.error('The selected files exceed the total maximum file size of: 10 mb.')
                    this.$refs.fileinput.reset()
                    this.files = null
                    return
                }
            }

            this.files = files
        },
        sendFeedback () {
            if (this.topic === '') {
                this.$toasted.error('Topic required')
            } else if (this.type == null) {
                this.$toasted.error('Choose a feedback type')
            } else if (this.feedback === '') {
                this.$toasted.error('Feedback required')
            } else {
                var data = new FormData()
                data.append('topic', this.topic)
                data.append('ftype', this.type)
                data.append('feedback', this.feedback)
                data.append('user_agent', navigator.userAgent)
                if (this.files != null) {
                    for (var i = 0; i < this.files.length; i++) {
                        data.append('files', this.files[i])
                    }
                }

                feedback.sendFeedback(data)
                    .then(response => { this.$toasted.success(response.data.description) })
                    .catch(error => { this.$toasted.error(error.response.data.description) })
            }
        }
    }

}
</script>
