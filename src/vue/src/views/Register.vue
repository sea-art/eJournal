<template>
    <content-single-column>
        <bread-crumb>&nbsp;</bread-crumb>
        <register-user v-if="!accountCreated" @handleAction="accountCreated=true"/>
        <b-card v-if="accountCreated" class="blue-border no-hover">
            <b-form @submit.prevent="verifyEmail">
                <b-input class="multi-form theme-input" v-model="emailVerificationToken" required placeholder="Email verification token"/>
                <b-button class="float-right multi-form add-button" type="submit">
                    <icon name="save"/>
                    Submit
                </b-button>
            </b-form>
        </b-card>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import icon from 'vue-awesome/components/Icon'
import registerUser from '@/components/account/RegisterUser.vue'
import userAPI from '@/api/user'

export default {
    name: 'Register',
    components: {
        'content-single-column': contentSingleColumn,
        'bread-crumb': breadCrumb,
        'register-user': registerUser,
        icon
    },
    data () {
        return {
            accountCreated: false,
            emailVerificationToken: null
        }
    },
    methods: {
        verifyEmail () {
            userAPI.verifyEmail(this.emailVerificationToken)
                .then(response => {
                    this.$toasted.success(response.data.description)
                    this.$router.push({ name: 'Home' })
                })
                .catch(error => { this.$toasted.error(error.response.data.description) })
        }
    }
}
</script>
