<template>
    <b-row>
        <b-col lg="4" md="12">
            <img class="profile-portrait" :src="image">
        </b-col>
        <b-col lg="8" md="12">
            <h2>User data</h2>
            <b-form-input v-model="username" type="text"></b-form-input>
            <b-form-input v-model="first_name" type="text"></b-form-input>
            <b-form-input v-model="last_name" type="text"></b-form-input>
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
            file: null
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
        }
        // updateProfilePicture () {
        //     userAPI.updateProfilePicture(this.$refs.file)
        // }
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
        // }
    }
}
</script>

<style>
.profile-portrait {
    max-height: 250px;
    border-radius: 50%!important;
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
