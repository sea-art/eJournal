<template>
    <b-button
        @click="fileDownload">
        <icon name="download"/>
        {{ fileName }}
    </b-button>
</template>

<script>
import icon from 'vue-awesome/components/Icon'
import userAPI from '@/api/user.js'

export default {
    props: {
        fileName: {
            required: true,
            String
        }
    },
    components: {
        'icon': icon
    },
    methods: {
        base64ToArrayBuffer (base64) {
            var binaryString = window.atob(base64)
            var len = binaryString.length
            var bytes = new Uint8Array(len)
            for (var i = 0; i < len; i++) {
                bytes[i] = binaryString.charCodeAt(i)
            }
            return bytes.buffer
        },
        fileDownload (e) {
            userAPI.getUserFile(this.fileName)
                .then(response => {
                    let blob = new Blob([this.base64ToArrayBuffer(response.data)], { type: response.headers['content-type'] })
                    let link = document.createElement('a')
                    link.href = window.URL.createObjectURL(blob)
                    link.download = /filename=(.*)/.exec(response.headers['content-disposition'])[1]
                    link.click()
                })
                .catch(_ => {
                    this.$toasted.error('Something went wrong while downloading your file.')
                })
        }
    }
}
</script>
