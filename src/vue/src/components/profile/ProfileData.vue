<template>
    <b-row>
        <b-col md="5" sm="12" class="text-center">
            <img class="profile-portrait" :src="image">
        </b-col>
        <b-col md="7" sm="12">
            <h2 class="mb-2">User data</h2>
            <b-form-input v-model="uname" type="text"/>
            <b-form-input v-model="first" type="text"/>
            <b-form-input v-model="last" type="text"/>
            <b-form-file
                ref="file"
                accept="image/*"
                v-on:change="updateProfilePicture"
                class="fileinput"
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
