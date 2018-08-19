<template>
    <content-single-column>
        <h1>Email Verification</h1>
        <b-card class="blue-border no-hover">
            <div class="center-content">
                <h2>Verifying</h2><br/>
                <icon name="spinner" pulse scale="1.5"/>
            </div>
        </b-card>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import icon from 'vue-awesome/components/Icon'
import userAPI from '@/api/user.js'

export default {
    name: 'EmailVerification',
    props: ['token'],
    mounted () {
        userAPI.verifyEmail(this.token)
            .then(response => {
                this.$toasted.success(response.data.result)
                this.$router.push({ name: 'Home' })
            })
            .catch(response => {
                this.$toasted.error(response.response.data.description)
                this.$router.push({
                    name: 'ErrorPage',
                    params: {
                        code: response.response.status,
                        message: response.response.data.result,
                        description: response.response.data.description
                    }
                })
            })
    },
    components: {
        'content-single-column': contentSingleColumn,
        icon
    }
}
</script>

<style lang="sass">
.center-content
    text-align: center

.center-content h2
    text-align: center
</style>
