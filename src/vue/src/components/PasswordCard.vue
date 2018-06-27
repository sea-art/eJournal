<template>
    <b-container no-gutters>
        <b-row>
            <h3 class="profile-title">Change password</h3><br/>
        </b-row>
        <b-row>
            <alert-box v-if="response" :type="response.type" :description="response.description"/>
        </b-row>
        <b-row>
            <b-col class="profile-col" cols="4">
                <span class="profile-password">Old password:</span>
            </b-col>
            <b-col cols="7">
                <b-form-input v-model="oldPass" type="password"></b-form-input><br/>
            </b-col>
        </b-row>

        <b-row>
            <b-col class="profile-col" cols="4">
                <span class="profile-password">New password:</span>
            </b-col>
            <b-col cols="7">
                <b-form-input v-model="newPass" type="password"></b-form-input><br/>
            </b-col>
        </b-row>

        <b-row>
            <b-col class="profile-col" cols="4">
                <span class="profile-password">Repeat new password:</span>
            </b-col>
            <b-col cols="7">
                <b-form-input v-model="newPassRepeat" type="password"></b-form-input>
            </b-col>
        </b-row>

        <b-row>
            <b-button @click="changePassword">Change password</b-button>
        </b-row>
    </b-container>
</template>

<script>
import auth from '@/api/auth'
import alert from '@/components/Alert.vue'

export default {
    components: {
        'alert-box': alert
    },
    data () {
        return {
            checkbox: false,
            oldPass: '',
            newPass: '',
            newPassRepeat: '',
            response: null
        }
    },
    methods: {
        changePassword: function () {
            if (this.newPass === this.newPassRepeat) {
                this.test = true
                auth.changePassword(this.newPass, this.oldPass)
                    .then(response => {
                        this.response = response.data
                        this.response['type'] = 'success'
                    })
                    .catch(response => {
                        this.response = response.response.data
                        this.response['type'] = 'danger'
                    })
            } else {
                this.test = false
                this.$toasted.error('Passwords do not match')
            }
        }
    }
}

</script>
