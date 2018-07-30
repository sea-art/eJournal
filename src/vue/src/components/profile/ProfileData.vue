<template>
    <b-row>
        <b-col md="5" sm="12" class="text-center">
            <div class="profile-portrait small-shadow">
                <img :src="profileImageDataURL">
                <!-- TODO Add cropping tool to help with the square aspect ratio Croppa seems most active and a solid choice -->
                <b-button @click="$refs.file.click()">
                    <icon name="upload"/>
                    Upload
                </b-button>
                <input
                    class="fileinput"
                    @change="fileHandler"
                    ref="file"
                    accept="image/*"
                    style="display: none"
                    type="file"/>

            </div>
        </b-col>
        <b-col md="7" sm="12">
            <h2 class="mb-2">User details</h2>
            <b-form-input class="theme-input multi-form" v-model="uname" type="text"/>
            <b-form-input class="theme-input multi-form" v-model="first" type="text"/>
            <b-form-input class="theme-input multi-form" v-model="last" type="text"/>

            <b-button class="add-button multi-form float-right" @click="saveUserdata">
                <icon name="save"/>
                Save
            </b-button>
            <b-button class="multi-form" @click="downloadUserData">
                <icon name="download"/>
                Download Data
            </b-button>
        </b-col>
    </b-row>
</template>

<script>
import userAPI from '@/api/user.js'
import icon from 'vue-awesome/components/Icon'

export default {
    props: ['uname', 'first', 'last', 'id', 'image'],
    data () {
        return {
            file: null,
            profileImageDataURL: null
        }
    },
    methods: {
        saveUserdata () {
            userAPI.updateUserData(this.uname, this.first, this.last)
                .then(this.$toasted.success('Saved profile data'))
        },
        fileHandler (e) {
            let maxSize = 2 * 1024 * 1024

            let files = e.target.files

            if (!files.length) { return }
            if (files[0].size > maxSize) {
                this.$toasted.error('The profile picture exceeds the maximum file size of 2MB.')
                return
            }

            var vm = this

            var reader = new FileReader()
            reader.onload = () => {
                var dataURL = reader.result

                var img = new Image()
                img.onload = () => {
                    if (img.width !== img.height) {
                        this.$toasted.error('Please submit a square image.')
                    } else {
                        userAPI.updateProfilePictureBase64(dataURL)
                            .then(response => {
                                vm.profileImageDataURL = dataURL
                            })
                            .catch(_ => {
                                this.$toasted.error('Something went wrong while uploading your profile picture.')
                            })
                    }
                }
                img.src = dataURL
            }
            reader.readAsDataURL(files[0])
        },
        downloadUserData () {
            userAPI.getUserData(this.id).then(data => {
                /* This is a way to download data. */
                /* Stringify the data and create a data blob of it. */
                data = JSON.stringify(data)
                const blob = new Blob([data], {type: 'text/plain'})

                /* Create a link to download the data and bind the data to it. */
                var downloadElement = document.createElement('a')
                downloadElement.download = 'userdata_of_' + this.uname + '.json'
                downloadElement.href = window.URL.createObjectURL(blob)
                downloadElement.dataset.downloadurl = ['text/json',
                    downloadElement.download, downloadElement.href].join(':')

                /* Create a click event and click on the download link to download the code. */
                const clickEvent = document.createEvent('MouseEvents')
                clickEvent.initEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null)
                downloadElement.dispatchEvent(clickEvent)
            })
        }
    },
    components: {
        'icon': icon
    },
    created () {
        this.profileImageDataURL = this.image
    }
}
</script>

<style lang="sass">
.profile-portrait
    display: inline-block
    position: relative
    width: 100%
    max-width: 250px
    margin-bottom: 20px
    border-radius: 50% !important
    overflow: hidden
    img
        position: absolute
        height: 100%
        width: 100%
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
</style>
