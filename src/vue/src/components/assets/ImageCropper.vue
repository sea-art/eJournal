<template>
    <b-card class="no-hover">
        <div class="profile-portrait-edit small-shadow">
            <croppa v-model="croppa"
                disable-click-to-choose
                :width="250"
                :height="250"
                canvas-color="transparent"
                :show-remove-button="false"
                :show-loading="true"
                :loading-size="50"
                accept="image/*"
                :file-size-limit="this.$root.maxFileSizeBytes"
                @file-type-mismatch="onFileTypeMismatch"
                @file-size-exceed="onFileSizeExceed"
                :initial-image="pictureUrl"
                initial-size="natural"
                initial-position="center"/>
        </div>
        <b-button @click="croppa.chooseFile()">
            <icon name="upload"/>
            Upload
        </b-button>
        <b-button class="change-button" @click="refreshPicture()">
            <icon name="undo"/>
            Reset
        </b-button>
        <b-button class="add-button float-right" @click="savePicture()">
            <icon name="save"/>
            Save
        </b-button>
    </b-card>
</template>

<script>
import icon from 'vue-awesome/components/Icon'

export default {
    name: 'ImageCropper',
    props: ['pictureUrl', 'refresh'],
    components: {
        icon
    },
    data () {
        return {
            croppa: {}
        }
    },
    watch: {
        refresh: function () {
            this.refreshPicture()
        }
    },
    methods: {
        onFileTypeMismatch (file) {
            this.$toasted.error('Invalid file type. Please choose an image.')
        },
        onFileSizeExceed (file) {
            this.$toasted.error('The profile picture exceeds the maximum file size of ' + this.$root.maxFileSizeBytes + ' bytes.')
        },
        savePicture () {
            this.$emit('newPicture', this.croppa.generateDataUrl('image/jpeg'))
        },
        refreshPicture () {
            this.croppa.refresh()
        }
    }
}
</script>

<style lang="sass">
@import '~sass/modules/breakpoints.sass'
@import '~sass/modules/colors.sass'

.profile-portrait-edit
    display: block
    position: relative
    width: 100%
    max-width: 250px
    max-height: 250px
    border-radius: 50% !important
    overflow: hidden
    margin: 0 auto
    margin-top: 10px
    margin-bottom: 20px
    .btn
        position: absolute
        width: 100%
        height: 25%
        bottom: -25%
        opacity: 0
    &:hover
        .btn
            bottom: 0px
            opacity: 1

.profile-portrait:after
    content: ""
    display: block
    padding-bottom: 100%

.croppa-container
    background-color: #000000
    height: 100%
    width: 100%
.croppa-container:hover
    opacity: 1
    background-color: #000000
</style>
