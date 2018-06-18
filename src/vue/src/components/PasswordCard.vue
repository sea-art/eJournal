<template>
    <b-container no-gutters>
        <b-row>
            <p class="profile-title">Change password</p><br/>
        </b-row>

        <b-row>
            <b-col class="profile-col" cols="4">
                <p class="profile-password">Old password:</p>
            </b-col>
            <b-col cols="7">
                <b-form-input class="passField" v-model="oldPass" type="password"></b-form-input><br/>
            </b-col>
        </b-row>

        <b-row>
            <b-col class="profile-col" cols="4">
                <p class="profile-password">New password:</p>
            </b-col>
            <b-col cols="7">
                <b-form-input class="passField" v-model="newPass" type="password"></b-form-input><br/>
            </b-col>
        </b-row>

        <b-row>
            <b-col class="profile-col" cols="4">
                <p class="profile-password">Repeat new password:</p>
            </b-col>
            <b-col cols="7">
                <b-form-input class="passField" v-model="newPassRepeat" type="password"></b-form-input>
            </b-col>
        </b-row>

        <b-row>
            <b-button @click="changePassword">Change password</b-button>
        </b-row>
    </b-container>
</template>

<script>
export default {
    data () {
        return {
            checkbox: false,
            oldPass: '',
            newPass: '',
            newPassRepeat: ''
        }
    },
    methods: {
        changePassword: function () {
            alert('I am a change password button!')
        }
    }
}

</script>

<style>
.passField {
    height: 30px;
}
</style>
