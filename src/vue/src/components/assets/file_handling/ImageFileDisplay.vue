<template>
    <div>
        <h5>
            {{ fileName }}
            <icon v-if="!show" @click.native="handleDownload" name="eye" class="action-icon"/>
            <icon v-if="show" @click.native="handleDownload" name="ban" class="crossed-icon"/>
            <icon v-if="show && fileURL" @click.native="downloadLink.click()" name="save" class="action-icon"/>
        </h5>
        <img v-if="show && fileURL" :src="fileURL">
    </div>
</template>

<script>
import userAPI from '@/api/user.js'
import icon from 'vue-awesome/components/Icon'
import dataHandling from '@/utils/data_handling.js'

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
            fileURL: null,
            downloadLink: null
        }
    },
    methods: {
        handleDownload () {
            this.show = !this.show

            if (!this.fileURL && this.show) {
                this.fileDownload()
            }
        },
        fileDownload () {
            userAPI.getUserFile(this.fileName, this.authorUID)
                .then(response => {
                    let blob = new Blob([dataHandling.base64ToArrayBuffer(response.data)], { type: response.headers['content-type'] })
                    this.fileURL = window.URL.createObjectURL(blob)

                    this.downloadLink = document.createElement('a')
                    this.downloadLink.href = this.fileURL
                    this.downloadLink.download = /filename=(.*)/.exec(response.headers['content-disposition'])[1]
                }, error => {
                    this.$toasted.error(error.response.data.description)
                })
                .catch(_ => {
                    this.$toasted.error('Error creating file.')
                })
        }
    },
    created () {
        this.show = this.display

        if (this.show) { this.fileDownload() }
    }
}
</script>
