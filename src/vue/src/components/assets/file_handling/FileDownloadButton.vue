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
        }
    },
    components: {
        icon
    },
    methods: {
        fileDownload (e) {
            userAPI.download(this.authorUID, this.fileName)
                .then(response => {
                    let blob = new Blob([dataHandling.base64ToArrayBuffer(response.data)], { type: response.headers['content-type'] })
                    let link = document.createElement('a')
                    link.href = window.URL.createObjectURL(blob)
                    link.download = /filename=(.*)/.exec(response.headers['content-disposition'])[1]
                    link.click()
                }, error => {
                    this.$toasted.error(error.response.data.description)
                })
                .catch(_ => {
                    this.$toasted.error('Error creating file.')
                })
        }
    }
}
</script>
