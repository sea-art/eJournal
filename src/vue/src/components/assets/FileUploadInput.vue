<template>
    <b-form-file
        :accept="acceptedFiletype"
        class="fileinput"
        @change="fileHandler"
        v-model="file"
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

            let formData = new FormData()
            formData.append('file', files[0])

            userAPI.updateUserFile(formData)
                .then(_ => {
                    this.$toasted.success('File upload success.')
                })
                .catch(response => {
                    this.$toasted.error(response.description)
                })
        }
    }
}
</script>
