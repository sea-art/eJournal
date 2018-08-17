<template>
    <div>
        <h5>
            {{ fileName }}
            <icon v-if="!show" @click.native="handleDownload" name="eye" class="action-icon"/>
            <icon v-if="show" @click.native="handleDownload" name="ban" class="crossed-icon"/>
        </h5>
        <img v-if="show && fileURL" :src="fileURL">
    </div>
</template>

<script>
import userAPI from '@/api/user.js'
import icon from 'vue-awesome/components/Icon'

export default {
    props: {
        fileName: {
            required: true,
            String
        },
        authorUID: {
            required: true,
            String
        },
        display: {
            default: false
        }
    },
    components: {
        icon
    },
    data () {
        return {
            show: false,
            fileURL: null
        }
    },
    methods: {
        handleDownload () {
            this.show = !this.show

            if (!this.fileURL && this.show) {
                this.fileDownload()
            }
        },
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
            userAPI.getUserFile(this.fileName, this.authorUID)
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
        this.show = this.display

        if (this.show) { this.fileDownload() }
    }
}
</script>
