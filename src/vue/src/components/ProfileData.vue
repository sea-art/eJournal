<template>
    <b-row>
        <b-col lg="4" md="12">
            <img :src="image">
        </b-col>
        <b-col lg="8" md="12">
            <h3>User data</h3>
            <b-form-input v-model="uname" type="text"></b-form-input>
            <span class="profile-data">Change profile picture</span>
            <b-form-file ref="file" v-on:change="updateProfilePicture" class="fileinput form-control" v-model="file" :state="Boolean(file)" placeholder="Upload profile picture..."></b-form-file>
            <b-button class="add-button" @click="saveUserdata">Save</b-button>
            <b-button @click="downloadUserData">Download Data</b-button>
        </b-col>
    </b-row>
</template>

<script>
import userAPI from '@/api/user.js'
export default {
    props: ['uname', 'id', 'image'],
    data () {
        return {
            file: null,
            username: ''
        }
    },
    methods: {
        saveUserdata () {
            userAPI.updateUserData(this.uname)
        },
        updateProfilePicture () {
            console.log(this.$refs.file)
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
    created () {
        this.username = this.uname
    }
}
</script>

<style>
.profile-picture {
    position: relative;
    width: 50%;
}

.fileinput {
    border-color: var(--theme-dark-grey)!important;
}

.fileinput label {
    /* border-style: none!important; */
    border: 1px var(--theme-light-grey) solid!important;
}
.fileinput input {
    background-color: var(--theme-light-grey)!important;
}
</style>
