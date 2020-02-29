<template>
    <div
        class="file-controls"
        @click="fileDownload"
    >
        <icon name="download"/>
        <i><span>{{ file.file_name }}</span></i>
    </div>
</template>

<script>
import auth from '@/api/auth.js'

export default {
    props: {
        file: {
            required: true,
        },
        authorUID: {
            required: true,
            String,
        },
        entryID: {
            required: true,
            String,
        },
        nodeID: {
            required: true,
            String,
        },
        contentID: {
            required: true,
            String,
        },
    },
    methods: {
        fileDownload () {
            auth.downloadFile(this.file.download_url)
                .then((response) => {
                    try {
                        const blob = new Blob([response.data], { type: response.headers['content-type'] })
                        const link = document.createElement('a')
                        link.href = window.URL.createObjectURL(blob)
                        link.download = this.file.file_name
                        document.body.appendChild(link)
                        link.click()
                        link.remove()
                    } catch (_) {
                        this.$toasted.error('Error creating file.')
                    }
                })
        },
    },
}
</script>

<style lang="sass">
.file-controls
    &:hover
        cursor: pointer
    span
        text-decoration: underline !important
    svg
        margin-bottom: -4px
</style>
