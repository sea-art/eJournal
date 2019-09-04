<template>
    <div
        class="file-controls"
        @click="fileDownload"
    >
        <icon name="download"/>
        <i><span>{{ fileName }}</span></i>
    </div>
</template>

<script>
import userAPI from '@/api/user.js'

export default {
    props: {
        fileName: {
            required: true,
            String,
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
            userAPI.download(this.authorUID, this.fileName, this.entryID, this.nodeID, this.contentID)
                .then((response) => {
                    try {
                        const blob = new Blob([response.data], { type: response.headers['content-type'] })
                        const link = document.createElement('a')
                        link.href = window.URL.createObjectURL(blob)
                        link.download = this.fileName
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
