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
                    let blob = new Blob([response.data], { type: response.headers['content-type'] })
                    let link = document.createElement('a')
                    link.href = window.URL.createObjectURL(blob)
                    link.download = this.fileName
                    document.body.appendChild(link)
                    link.click()
                    link.remove()
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
