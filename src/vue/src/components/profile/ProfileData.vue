<template>
    <b-row>
        <b-col md="5" sm="12" class="text-center">
            <div class="profile-portrait small-shadow">
                <img :src="image">
                <!-- TODO handle file uploads. The original profile picture upload did not work yet.
                <b-form-file ref="file" v-on:change="updateProfilePicture" class="fileinput form-control" v-model="file" :state="Boolean(file)" placeholder="Upload profile picture..."></b-form-file> -->
                <b-button>
                    <icon name="upload"/>
                    Upload
                </b-button>
            </div>
        </b-col>
        <b-col md="7" sm="12">
            <h2 class="mb-2">User details</h2>
            <b-form-input class="theme-input multi-form" v-model="uname" type="text"/>
            <b-form-input class="theme-input multi-form" v-model="first" type="text"/>
            <b-form-input class="theme-input multi-form" v-model="last" type="text"/>
            <b-button class="add-button multi-form" @click="saveUserdata">
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
            file: null
        }
    },
    methods: {
        saveUserdata () {
            userAPI.updateUserData(this.uname, this.first, this.last)
                .then(this.$toasted.success('Saved profile data'))
        },
        updateProfilePicture () {
            userAPI.updateProfilePicture(this.$refs.file)
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
