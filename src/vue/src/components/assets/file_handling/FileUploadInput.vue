<template>
    <b-form-file
        :accept="acceptedFiletype"
        class="fileinput"
        @change="fileHandler"
        :state="Boolean(file)"
        :placeholder="placeholderText" />
</template>

<script>
import auth from '@/api/auth'

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
    data () {
        return {
            placeholderText: 'No file chosen',
            file: null
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

            this.$emit('fileSelect', this.file.name)

            if (this.autoUpload) { this.uploadFile() }
        },
        uploadFile () {
            let formData = new FormData()
            formData.append('file', this.file)
            formData.append('assignment_id', this.aID)
            formData.append('content_id', this.contentID)

            auth.uploadFile(this.endpoint, formData, {customSuccessToast: 'File upload success.'})
                .then(() => {
                    this.$emit('fileUploadSuccess', this.file.name)
                })
                .catch(() => {
                    this.$emit('fileUploadFailed', this.file.name)
                    this.file = null
                })
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
