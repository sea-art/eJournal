<template>
    <b-row>
        <b-col md="5" sm="12" class="text-center">
            <img class="profile-portrait" :src="profileImage">
        </b-col>
        <b-col md="7" sm="12">
            <h2 class="mb-2">User data</h2>
            <b-form-input class="theme-input" v-model="uname" type="text"/>
            <b-form-input class="theme-input" v-model="first" type="text"/>
            <b-form-input class="theme-input" v-model="last" type="text"/>
            <b-form-file
                ref="file"
                accept="image/*"
                class="fileinput"
                @change="fileHandler"
                v-model="file"
                :state="Boolean(file)"
                placeholder="Change picture"/>

            <b-button class="add-button" @click="saveUserdata">Save</b-button>
            <b-button @click="downloadUserData">Download Data</b-button>
        </b-col>
    </b-row>
</template>

<script>
import userAPI from '@/api/user.js'

export default {
    props: ['uname', 'first', 'last', 'id', 'image'],
    data () {
        return {
            file: null,
            profileImage: null
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

            var reader = new FileReader()
            var vm = this

            reader.onload = (e) => {
                console.log('$$$%%% HERE')
                var image = new Image()
                console.log(image)
                image.src = e.target.result
                image.onload = function () {
                    if (image.height !== image.width) {
                        vm.$toasted.error('The profile picture should be a square image!')
                    } else {
                        // Image is the correct size and is symmetrical, lets send it to the backend.


                        userAPI.updateProfilePicture(formData)
                            .then(_ => { reader.readAsDataURL(image) })
                            .catch(_ => { vm.$toasted.error('Something went wrong while uploading your profile picture.') })
                    }
                }
            }
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
    created () {
        this.profileImage = this.image
    }
}
</script>

<style lang="sass">
@import '~sass/modules/colors.sass'

.profile-portrait
    max-width: 250px
    margin-bottom: 20px
    border-radius: 50% !important
</style>
