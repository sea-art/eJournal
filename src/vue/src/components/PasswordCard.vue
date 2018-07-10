<template>
    <div>
        <b-row>
            <b-col cols="12">
                <h2 class="profile-title">Change password</h2>
            </b-col>
        </b-row>
        <alert-box v-if="response" :type="response.type" :description="response.description"/>
        <b-input v-model="oldPass" type="password" placeholder="Old password"/>
        <b-input v-model="newPass" type="password" placeholder="New password"/>
        <b-input v-model="newPassRepeat" type="password" placeholder="Repeat new password"/>
        <b-button @click="changePassword">Change password</b-button>
    </div>
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
