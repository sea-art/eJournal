<template>
    <b-container no-gutters>
        <b-row>
            <h3 class="profile-title">Change password</h3><br/>
        </b-row>

        <b-row>
            <b-col class="profile-col" cols="4">
                <span class="profile-password">Old password:</span>
            </b-col>
            <b-col cols="7">
                <b-form-input class="passField" v-model="oldPass" type="password"></b-form-input><br/>
            </b-col>
        </b-row>

        <b-row>
            <b-col class="profile-col" cols="4">
                <span class="profile-password">New password:</span>
            </b-col>
            <b-col cols="7">
                <b-form-input class="passField" v-model="newPass" type="password"></b-form-input><br/>
            </b-col>
        </b-row>

        <b-row>
            <b-col class="profile-col" cols="4">
                <span class="profile-password">Repeat new password:</span>
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
import auth from '@/api/auth'

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
            if (this.newPass.match('(.*[A-Z]).*') && this.newPass.length > 3) {
                if (this.newPass === this.newPassRepeat) {
                    this.test = true
                    auth.changePassword(this.newPass, this.oldPass)
                } else {
                    this.test = false
                    alert('Password does not match')
                }
            } else {
                alert('Not a strong password')
            }
        }
    }
}

</script>

<style>
.passField {
    height: 30px;
}
</style>
