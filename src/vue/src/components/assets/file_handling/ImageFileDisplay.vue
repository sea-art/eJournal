<template>
    <div class="image-field">
        <div
            class="image-controls mb-2 unselectable"
            @click="handleDownload"
        >
            <icon
                name="image"
                class="shift-up-2"
            />
            <b class="ml-1">
                {{ file.file_name }}
            </b>
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
        display: {
            default: false,
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
        b
            text-decoration: underline !important
</style>
