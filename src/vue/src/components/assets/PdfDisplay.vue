<template>
    <div v-if="fileURL">
        <pdf :src="fileURL"/>
    </div>
</template>

<script>
import pdf from 'vue-pdf'
import userAPI from '@/api/user.js'

export default {
    props: {
        fileName: {
            required: true,
            String
        }
    },
    components: {
        pdf
    },
    data () {
        return {
            fileURL: null
        }
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
        fileDownload () {
            userAPI.getUserFile(this.fileName)
                .then(response => {
                    let blob = new Blob([this.base64ToArrayBuffer(response.data)], { type: response.headers['content-type'] })
                    this.fileURL = window.URL.createObjectURL(blob)
                })
                .catch(response => {
                    this.$toasted.error(response.description)
                })
        }
    },
    created () {
        this.fileDownload()
    }
}
</script>
