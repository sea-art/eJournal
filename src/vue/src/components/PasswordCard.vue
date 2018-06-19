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
import auth from '@/api/auth'

export default {
    data () {
        return {
            checkbox: false,
            oldPass: '',
            newPass: '',
            newPassRepeat: '',
            test: false
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
                    alert('Password is not matching')
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
