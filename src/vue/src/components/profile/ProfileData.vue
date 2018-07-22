<template>
    <b-row>
        <b-col md="5" sm="12" class="text-center">
            <img class="profile-portrait" :src="profileImage">
        </b-col>
        <b-col md="7" sm="12">
            <h2 class="mb-2">User data</h2>
            <b-form-input class="theme-input" v-model="username" type="text"/>
            <b-form-input class="theme-input" v-model="first_name" type="text"/>
            <b-form-input class="theme-input" v-model="last_name" type="text"/>
            <b-form-file
                ref="file"
                accept="image/*"
                class="fileinput"
                @change="fileHandler"
                v-model="file"
                :state="Boolean(file)"
                placeholder="Change picture"/>

            <b-button class="add-button" @click="saveUserdata">Save</b-button>
            <b-button>Download Data</b-button>
        </b-col>
    </b-row>
</template>

<script>
import auth from '@/api/auth.js'

export default {
    props: ['username', 'first_name', 'last_name', 'id', 'image'],
    data () {
        return {
            file: null,
            profileImage: null
        }
    },
    methods: {
        saveUserdata () {
            auth.update('users/' + this.id, {
                username: this.username,
                first_name: this.first_name,
                last_name: this.last_name
            })
                .then(response => this.$toasted.success(response.description))
        },
        fileHandler (e) {
            let files = e.target.files
            if (!files.length) { return }

            this.file = files[0]

            let formData = new FormData()
            formData.append('file', this.file)

            // userAPI.updateProfilePicture(formData)
            //     .then(_ => { this.setClientProfilePicture(this.file) })
            //     .catch(_ => { this.$toasted.error('Something went wrong while uploading your profile picture.') })
        },
        setClientProfilePicture (imageFile) {
            var reader = new FileReader()
            var vm = this

            reader.onload = (e) => {
                vm.profileImage = e.target.result
            }
            reader.readAsDataURL(imageFile)
        },
        // downloadUserData () {
        //     userAPI.getUserData(this.id).then(data => {
        //         /* This is a way to download data. */
        //         /* Stringify the data and create a data blob of it. */
        //         data = JSON.stringify(data)
        //         const blob = new Blob([data], {type: 'text/plain'})
        //
        //         /* Create a link to download the data and bind the data to it. */
        //         var downloadElement = document.createElement('a')
        //         downloadElement.download = 'userdata_of_' + this.uname + '.json'
        //         downloadElement.href = window.URL.createObjectURL(blob)
        //         downloadElement.dataset.downloadurl = ['text/json',
        //             downloadElement.download, downloadElement.href].join(':')
        //
        //         /* Create a click event and click on the download link to download the code. */
        //         const clickEvent = document.createEvent('MouseEvents')
        //         clickEvent.initEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null)
        //         downloadElement.dispatchEvent(clickEvent)
        //     })
        //         .then(response => this.$toasted.success(response.description))
        // }
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
