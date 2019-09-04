<template>
    <content-single-column>
        <h1><span>Email Verification</span></h1>
        <b-card class="no-hover">
            <div class="center-content">
                <h2 class="center-content">
                    Verifying
                </h2><br/>
                <icon
                    name="circle-o-notch"
                    pulse
                    scale="1.5"
                />
            </div>
        </b-card>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import userAPI from '@/api/user.js'

export default {
    name: 'EmailVerification',
    components: {
        contentSingleColumn,
    },
    props: ['username', 'token'],
    mounted () {
        userAPI.verifyEmail(this.username, this.token, { responseSuccessToast: true })
            .then(() => {
                this.$store.commit('user/EMAIL_VERIFIED')
                this.$router.push({ name: 'Home' })
            })
            .catch((error) => {
                this.$router.push({
                    name: 'ErrorPage',
                    params: {
                        code: error.response.status,
                        reasonPhrase: error.response.statusText,
                        description: error.response.data.description,
                    },
                })
            })
    },
}
</script>
