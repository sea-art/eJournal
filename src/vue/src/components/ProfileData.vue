<template>
    <b-row>
        <b-col lg="4" md="12">
            <img :src="image">
        </b-col>
        <b-col lg="8" md="12">
            <h3>User data</h3>
            <b-form-input v-model="name" type="text"></b-form-input>
            <span class="profile-data">Change profile picture</span>
            <b-form-file class="fileinput form-control" v-model="file" :state="Boolean(file)" placeholder="Upload profile picture..."></b-form-file>
            <b-button @click="saveUserdata">Save</b-button>
        </b-col>
    </b-row>
</template>

<script>
import userAPI from '@/api/user.js'
export default {
    props: ['name', 'id', 'image'],
    data () {
        return {
            file: null,
            saveUserdata () {

            }
        }
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
