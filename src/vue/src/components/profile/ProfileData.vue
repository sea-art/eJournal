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
            <b-form-input :readonly="true" class="theme-input multi-form" v-model="userData.username" type="text"/>
            <b-form-input :readonly="(userData.lti_id) ? true : false" class="theme-input multi-form" v-model="userData.first_name" type="text"/>
            <b-form-input :readonly="(userData.lti_id) ? true : false" class="theme-input multi-form" v-model="userData.last_name" type="text"/>

            <email :userData="userData"/>

            <b-button v-if="!userData.lti_id" class="add-button multi-form float-right" @click="saveUserdata">
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
import email from '@/components/profile/Email.vue'
import dataHandling from '@/utils/data_handling.js'

export default {
    props: ['userData'],
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
            emailVerificationTokenMessage: null
        }
    },
    methods: {
        saveUserdata () {
            auth.update('users/' + this.userData.id, this.userData)
                .then(_ => { this.$toasted.success('Saved profile data') })
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
                            .then(_ => { vm.profileImageDataURL = dataURL })
                            .catch(error => { this.$toasted.error(error.response.data.description) })
                    }
                }
                img.src = dataURL
            }
            reader.readAsDataURL(files[0])
        },
        downloadUserData () {
            auth.get('user/' + this.userData.id + '/download')
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
    },
    mounted () {
        this.profileImageDataURL = this.userData.picture
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
