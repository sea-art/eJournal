<template>
    <content-single-column>
        <bread-crumb>&nbsp;</bread-crumb>
        <b-card v-if="userData" class="no-hover blue-border">
            <profile-data :userData="userData"/>
            <notification-card :userData="userData"/>
            <password-card/>
        </b-card>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import profileData from '@/components/profile/ProfileData.vue'
import notificationCard from '@/components/profile/NotificationCard.vue'
import passwordCard from '@/components/profile/PasswordCard.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import userAPI from '@/api/user.js'

export default {
    name: 'Profile',
    data () {
        return {
            userData: null
        }
    },
    components: {
        'content-single-column': contentSingleColumn,
        'bread-crumb': breadCrumb,
        'profile-data': profileData,
        'notification-card': notificationCard,
        'password-card': passwordCard
    },
    created () {
        userAPI.getOwnUserData()
            .then(userData => { this.userData = userData })
            .catch(response => { this.$toasted.error(response.data.description) })
    }
}
</script>
