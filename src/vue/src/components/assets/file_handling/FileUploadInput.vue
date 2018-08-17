<template>
    <b-form-file
        :accept="acceptedFiletype"
        class="fileinput"
        @change="fileHandler"
        :state="Boolean(file)"
        placeholder="Select a file."/>
</template>

<script>
import userAPI from '@/api/user.js'

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
        jID: {
            required: true,
            String
        },
        autoUpload: {
            default: false
        }
    },
    data () {
        return {
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
            formData.append('jID', this.jID)

            userAPI.updateUserFile(formData)
                .then(_ => {
                    this.$emit('fileUploadSuccess', this.file.name)
                    this.$toasted.success('File upload success.')
                })
                .catch(response => {
                    this.$emit('fileUploadFailed', [this.file.name, response.description])
                    this.$toasted.error(response.description)
                    this.file = null
                })
        }
    }
}
</script>
