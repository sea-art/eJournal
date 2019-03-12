<template>
    <div>
        <b-modal
            ref="cropperModal"
            title="Edit profile picture"
            hide-footer>
                <cropper v-if="this.profileImageDataURL" ref="cropperRef" :pictureUrl="this.profileImageDataURL" @newPicture="fileHandler"/>
        </b-modal>
        <div class="profile-picture-lg">
            <img :src="storeProfilePic">
            <b-button @click="showCropperModal()">
                <icon name="edit"/>
                Edit
            </b-button>
        </div>
        <h4 class="mb-2 d-block"><span>User details</span></h4>
        <b-card class="no-hover multi-form" :class="$root.getBorderClass($route.params.uID)">
            <h2 class="field-heading multi-form">Username</h2>
            <b-form-input :readonly="true" class="theme-input multi-form" :value="storeUsername" type="text"/>
            <h2 class="field-heading multi-form">Full name</h2>
            <b-form-input :readonly="(storeLtiID) ? true : false"
                class="theme-input multi-form"
                v-model="fullName"
                type="text"
                placeholder="Full name"/>
            <h2 class="field-heading multi-form">Email address</h2>
            <email/>

            <b-button v-if="!storeLtiID" class="add-button multi-form float-right" @click="saveUserdata">
                <icon name="save"/>
                Save
            </b-button>
            <b-button class="multi-form" @click="downloadUserData">
                <icon name="download"/>
                Download Data
            </b-button>
        </b-card>
    </div>
</template>

<script>
import email from '@/components/profile/Email.vue'
import userAPI from '@/api/user'
import icon from 'vue-awesome/components/Icon'
import cropper from '@/components/assets/ImageCropper'
import { mapGetters } from 'vuex'

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
            fullName: null,
            updateCropper: false
        }
    },
    computed: {
        ...mapGetters({
            storeUsername: 'user/username',
            storeLtiID: 'user/ltiID',
            storeProfilePic: 'user/profilePicture',
            storeFullName: 'user/fullName'
        })
    },
    methods: {
        showCropperModal () {
            this.$refs.cropperRef.refreshPicture()
            this.$refs['cropperModal'].show()
        },
        saveUserdata () {
            userAPI.update(0, {full_name: this.fullName}, {customSuccessToast: 'Saved profile data.'})
                .then(() => {
                    this.$store.commit('user/SET_FULL_USER_NAME', {fullName: this.fullName})
                })
        },
        fileHandler (dataURL) {
            userAPI.updateProfilePictureBase64(dataURL, {customSuccessToast: 'Profile picture updated.'})
                .then(() => {
                    this.$store.commit('user/SET_PROFILE_PICTURE', dataURL)
                    this.profileImageDataURL = dataURL
                    this.$refs['cropperModal'].hide()
                })
        },
        downloadUserData () {
            userAPI.GDPR(0)
                .then(response => {
                    try {
                        let blob = new Blob([response.data], { type: response.headers['content-type'] })
                        let link = document.createElement('a')
                        link.href = window.URL.createObjectURL(blob)
                        link.download = this.storeUsername + '_all_user_data.zip'
                        document.body.appendChild(link)
                        link.click()
                        link.remove()
                    } catch (_) {
                        this.$toasted.error('Error creating file locally.')
                    }
                })
        },
        isChanged () {
            return (this.fullName !== this.storeFullName)
        }
    },
    mounted () {
        this.profileImageDataURL = this.storeProfilePic
        this.fullName = this.storeFullName
    }
}
</script>
