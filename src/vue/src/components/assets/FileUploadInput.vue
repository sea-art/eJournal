<template>
    <input
        class="fileinput"
        @change="fileHandler"
        :ref="'file' + id"
        :accept="acceptedFiletype"
        type="file"/>
</template>

<script>
import userAPI from '@/api/user.js'

export default {
    props: {
        id: {
            required: true,
            String
        },
        acceptedFiletype: {
            required: true,
            String
        },
        maxSizeBytes: {
            required: true,
            Number
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
                .then(response => {
                    this.$toasted.success('File upload success.')
                })
                .catch(_ => {
                    this.$toasted.error('Something went wrong uploading your file')
                })
        }
    }
}
</script>

<style lang="sass">
</style>
