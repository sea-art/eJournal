<template>
    <b-row>
        <b-col md="5" sm="12" class="text-center">
            <div class="profile-portrait small-shadow">
                <img :src="userData.profile_picture">
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
            <b-form-input :readonly="true" class="theme-input multi-form" :value="$store.getters['user/username']" type="text"/>
            <b-form-input :readonly="($store.getters['user/ltiID']) ? true : false" class="theme-input multi-form" v-model="firstName" type="text"/>
            <b-form-input :readonly="($store.getters['user/ltiID']) ? true : false" class="theme-input multi-form" v-model="lastName" type="text"/>
            <email/>

            <b-button v-if="!$store.getters['user/ltiID']" class="add-button multi-form float-right" @click="saveUserdata">
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
import email from '@/components/profile/Email.vue'

import userAPI from '@/api/user'
import dataHandling from '@/utils/data_handling.js'
import icon from 'vue-awesome/components/Icon'

export default {
    components: {
        icon,
        email
    },
    data () {
        return {
            file: null,
            profileImageDataURL: null,
            showEmailValidationInput: true,
            emailVerificationToken: null,
            emailVerificationTokenMessage: null,
            firstName: null,
            lastName: null
        }
    },
    methods: {
        saveUserdata () {
            userAPI.update(0, {first_name: this.firstName, last_name: this.lastName})
                .then(_ => {
                    this.$store.commit('user/SET_FULL_USER_NAME', { firstName: this.firstName, lastName: this.lastName })
                    this.$toasted.success('Saved profile data')
                })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        },
        fileHandler (e) {
            let files = e.target.files

            if (!files.length) { return }
            if (files[0].size > this.$root.maxFileSizeBytes) {
                this.$toasted.error('The profile picture exceeds the maximum file size of ' + this.$root.maxFileSizeBytes + ' bytes.')
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
                            .then(_ => {
                                vm.$store.commit('user/SET_PROFILE_PICTURE', dataURL)
                                vm.profileImageDataURL = dataURL
                            })
                            .catch(error => { this.$toasted.error(error.response.data.description) })
                    }
                }
                img.src = dataURL
            }
            reader.readAsDataURL(files[0])
        },
        downloadUserData () {
            userAPI.GDPR()
                .then(response => {
                    let blob = new Blob([response.data], { type: response.headers['content-type'] })
                    let link = document.createElement('a')
                    link.href = window.URL.createObjectURL(blob)
                    link.download = this.$store.getters['user/username'] + '_all_user_data.zip'
                    document.body.appendChild(link)
                    link.click()
                    link.remove()
                }, error => {
                    this.$toasted.error(error.response.data.description)
                })
                .catch(e => {
                    this.$toasted.error('Error creating file.')
                })
        }
    },
    mounted () {
        this.profileImageDataURL = this.$store.getters['user/profilePicture']
        this.firstName = this.$store.getters['user/firstName']
        this.lastName = this.$store.getters['user/lastName']
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
