<template>
    <div class="image-field">
        <div class="image-controls mb-2 unselectable" @click="handleDownload">
            <icon name="file-image"/>
            <i><span>{{ fileName }}</span></i>
        </div>
        <img :class="showImage()" v-if="fileURL" :src="fileURL">
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
        showImage () {
            return this.show ? 'open' : 'closed'
        },
        fileDownload () {
            userAPI.getUserFile(this.fileName, this.authorUID)
                .then(response => {
                    let blob = new Blob([dataHandling.base64ToArrayBuffer(response.data)], { type: response.headers['content-type'] })
                    this.fileURL = window.URL.createObjectURL(blob)
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

<style lang="sass">
@import '~sass/modules/colors.sass'

.closed
    max-height: 0px
    -webkit-transition: height, .6s linear
    -moz-transition: height, .6s linear
    -ms-transition: height, .6s linear
    -o-transition: height, .6s linear
    transition: height, .6s linear

.open
    max-height: 100vh
    -webkit-transition: height, .6s linear
    -moz-transition: height, .6s linear
    -ms-transition: height, .6s linear
    -o-transition: height, .6s linear
    transition: height, .6s linear

.image-field
    img
        display: inline
    .image-controls
        &:hover
            cursor: pointer
        span
            text-decoration: underline !important
        svg
            margin-bottom: -2px
</style>
