<template>
    <div>
        <h2 class="mb-2">Change password</h2>
        <b-input class="theme-input multi-form" v-model="oldPass" type="password" placeholder="Old password"/>
        <b-input class="theme-input multi-form" v-model="newPass" type="password" placeholder="New password"/>
        <b-input class="theme-input multi-form" v-model="newPassRepeat" type="password" placeholder="Repeat new password"/>
        <b-button @click="changePassword" class="add-button">
            <icon name="save"/>
            Save
        </b-button>
    </div>
</template>

<script>
import auth from '@/api/auth'
import icon from 'vue-awesome/components/Icon'

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
            if (this.newPass === this.newPassRepeat) {
                auth.changePassword(this.newPass, this.oldPass)
                    .then(response => {
                        this.$toasted.success('Password updated successfully')
                    })
                    .catch(response => {
                        this.$toasted.error('Something went wrong updating your password, please try again.')
                    })
            } else {
                this.$toasted.error('Passwords do not match')
            }
        }
    },
    components: {
        'icon': icon
    }
}
</script>
