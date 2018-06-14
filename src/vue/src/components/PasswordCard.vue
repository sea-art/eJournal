<template>
    <b-container>
        <b-row>
            <h8>Notification-emails</h8><br/>
        </b-row>
        <b-row>
            <b-col cols="3">
                <p class="profile-password">Old password</p>
                <p class="profile-password">New password</p>
                <p class="profile-password">Repeat new password</p>
            </b-col>
            <b-col class="notification-body" cols="3">
                <password-field></password-field>
                <password-field></password-field>
                <password-field></password-field>
            </b-col>
            <b-col cols="6"></b-col>
        </b-row>
    </b-container>
</template>

<script>
import PasswordField from '@/components/passwordComponent.vue'

export default {
    components: {
        'password-field': PasswordField
    },
    data () {
        return {
            checkbox: false
        }
    }
}

</script>

<style>
.notifcatian {line-height: 10px;}

.col-3 {padding-left: 0px;}
</style>
