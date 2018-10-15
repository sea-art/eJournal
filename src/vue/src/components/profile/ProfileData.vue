<template>
    <b-row>
        <b-col md="5" sm="12" class="text-center">
            <b-modal
                ref="cropperModal"
                title="Edit your profile picture"
                hide-footer>
                    <cropper v-if="this.profileImageDataURL" :pictureUrl="this.profileImageDataURL" @newPicture="fileHandler" :refresh="updateCropper"/>
            </b-modal>
            <div class="profile-portrait small-shadow">
                <img :src="$store.getters['user/profilePicture']">
                <b-button @click="showCropperModal()">
                    <icon name="edit"/>
                    Edit
                </b-button>
            </div>
        </b-col>
        <b-col md="7" sm="12">
            <h2 class="mb-2">User details</h2>
            <b-form-input :readonly="true" class="theme-input multi-form input-disabled" :value="$store.getters['user/username']" type="text"/>
            <b-form-input :readonly="($store.getters['user/ltiID']) ? true : false"
                :class="{'input-disabled': ($store.getters['user/ltiID']) ? true : false}"
                class="theme-input multi-form"
                v-model="firstName"
                type="text"
                placeholder="First name"/>
            <b-form-input :readonly="($store.getters['user/ltiID']) ? true : false"
                :class="{'input-disabled': ($store.getters['user/ltiID']) ? true : false}"
                class="theme-input multi-form"
                v-model="lastName"
                type="text"
                placeholder="Surname"/>
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
import icon from 'vue-awesome/components/Icon'

import cropper from '@/components/assets/ImageCropper'

export default {
    components: {
        icon,
        email,
        cropper
    },
    data () {
        return {
            file: null,
            profileImageDataURL: null,
            showEmailValidationInput: true,
            emailVerificationToken: null,
            emailVerificationTokenMessage: null,
            firstName: null,
            lastName: null,
            updateCropper: false
        }
    },
    methods: {
        showCropperModal () {
            this.updateCropper = !this.updateCropper
            this.$refs['cropperModal'].show()
        },
        hideCropper (ref) {
            this.$refs[ref].hide()
        },
        saveUserdata () {
            userAPI.update(0, {first_name: this.firstName, last_name: this.lastName})
                .then(_ => {
                    this.$store.commit('user/SET_FULL_USER_NAME', { firstName: this.firstName, lastName: this.lastName })
                    this.$toasted.success('Saved profile data.')
                })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        },
        fileHandler (dataURL) {
            userAPI.updateProfilePictureBase64(dataURL)
                .then(_ => {
                    this.$store.commit('user/SET_PROFILE_PICTURE', dataURL)
                    this.profileImageDataURL = dataURL
                    this.$toasted.success('Profile picture updated.')
                })
                .catch(error => { this.$toasted.error(error.response.data.description) })
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
        },
        isChanged () {
            if (this.firstName !== this.$store.getters['user/firstName'] || this.lastName !== this.$store.getters['user/lastName']) {
                return true
            }

            return false
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
@import '~sass/modules/breakpoints.sass'

.profile-portrait
    display: inline-block
    position: relative
    width: 100%
    max-width: 250px
    margin-bottom: 20px
    border-radius: 50% !important
    overflow: hidden
    @include lg
        left: 10px
        top: 20px
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
