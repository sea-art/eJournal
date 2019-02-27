<template>
    <div>
        <b-form-file
        ref="bonusInput"
            :accept="acceptedFiletype"
            class="fileinput"
            @change="fileHandler"
            :state="Boolean(file)"
            :placeholder="placeholderText" />
        <b-button
            v-if="!autoUpload"
            class="add-button multi-form float-right"
            @click="uploadFile">
            <icon name="upload"/>
            Upload
        </b-button>

        <div v-if="errorLogs">
            <b class="text-red">Errors in file:</b>
            <b v-if="errorLogs.general">
                {{ errorLogs.general }}
            </b>
            <div v-if="errorLogs.unknown_users">
                <b>The following users do not exist:</b><br/>
                <span v-for="(username, lineNumber) in errorLogs.unknown_users" :key="`unknown-users-${lineNumber}-${username}`">
                    <b>&emsp;&emsp;&emsp;{{ lineNumber }})</b> {{ username }}<br/>
                </span>
            </div>
            <div v-if="errorLogs.incorrect_format_lines">
                <b>The following lines are incorrectly formatted:</b><br/>
                <span v-for="(content, lineNumber) in errorLogs.incorrect_format_lines" :key="`incorrect-format-${lineNumber}-${content}`">
                    <b>&emsp;&emsp;&emsp;{{ lineNumber }})</b> {{ content }}<br/>
                </span>
            </div>
            <div v-if="errorLogs.duplicates">
                <b>The following users occur twice:</b><br/>
                <span v-for="(username, lineNumber) in errorLogs.duplicates" :key="`duplicates-${lineNumber}-${username}`">
                    <b>&emsp;&emsp;&emsp;{{ lineNumber }})</b> {{ username }}<br/>
                </span>
            </div>
        </div>
    </div>
</template>

<script>
import auth from '@/api/auth'
import icon from 'vue-awesome/components/Icon'

export default {
    props: {
        acceptedFiletype: {
            required: true,
            String
        },
        maxSizeBytes: {
            required: true,
            Number
        },
        aID: {
            required: true,
            String
        },
        autoUpload: {
            default: false,
            Boolean
        },
        endpoint: {
            default: 'users/upload'
        },
        placeholder: {
            default: 'No file chosen'
        },
        contentID: {
            default: null
        }
    },
    components: {
        icon
    },
    data () {
        return {
            placeholderText: 'No file chosen',
            file: null,
            errorLogs: null
        }
    },
    methods: {
        fileHandler (e) {
            let files = e.target.files

            if (!files.length) { return }
            if (files[0].size > this.maxSizeBytes) {
                this.$toasted.error('The selected file exceeds the maximum file size of: ' + this.maxSizeBytes + ' bytes.')
                return
            }

            this.file = files[0]
            this.resetErrorLogs()

            this.$emit('fileSelect', this.file.name)

            if (this.autoUpload) { this.uploadFile() }
        },
        uploadFile () {
            let formData = new FormData()
            formData.append('file', this.file)
            formData.append('assignment_id', this.aID)
            formData.append('content_id', this.contentID)

            auth.uploadFileEmail(this.endpoint, formData, {
                customSuccessToast: 'Successfully imported bonus points.',
                customErrorToast: 'Something is wrong with the uploaded file.'
            })
                .then(() => {
                    this.$emit('bonusPointsSuccesfullyUpdated', this.file.name)
                    this.file = null
                    this.$refs['bonusInput'].reset()
                })
                .catch(error => {
                    this.$emit('bonusPointsFileFormatIssues', this.file.name)
                    this.file = null
                    this.$refs['bonusInput'].reset()
                    this.errorLogs = error.response.data.description
                })
        },
        resetErrorLogs () {
            this.errorLogs = null
        }
    },
    created () {
        // Assume the given file is present in the backend
        if (this.placeholder !== null && this.placeholder !== 'No file chosen') {
            this.file = true
            this.placeholderText = this.placeholder
        }
    }
}
</script>
