<template>
    <div class="image-field">
        <div
            class="image-controls mb-2 unselectable"
            @click="handleDownload"
        >
            <icon name="image"/>
            <i><span>{{ file.file_name }}</span></i>
        </div>
        <transition name="fade">
            <img
                v-if="fileURL && show"
                class="theme-img"
                :class="showImage"
                :src="fileURL"
            />
        </transition>
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
        display: {
            default: false,
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
    data () {
        return {
            show: false,
            fileURL: null,
        }
    },
    computed: {
        showImage () {
            return this.show ? 'open' : 'closed'
        },
    },
    created () {
        this.show = this.display

        if (this.show) { this.fileDownload() }
    },
    methods: {
        handleDownload () {
            this.show = !this.show

            if (!this.fileURL && this.show) {
                this.fileDownload()
            }
        },
        fileDownload () {
            auth.downloadFile(this.file.download_url)
                .then((response) => {
                    try {
                        const blob = new Blob([response.data], { type: response.headers['content-type'] })
                        this.fileURL = window.URL.createObjectURL(blob)
                    } catch (_) {
                        this.$toasted.error('Error creating file.')
                    }
                })
        },
    },
    destroy () { this.downloadLink.remove() },
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'

.closed
    -webkit-transition: height, .6s linear

.open
    max-height: 100vh
    -webkit-transition: height, .6s linear

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
