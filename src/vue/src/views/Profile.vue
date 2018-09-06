<template>
    <content-single-column>
        <bread-crumb>&nbsp;</bread-crumb>
        <b-card class="no-hover blue-border">
            <profile-data/>
            <notification-card/>
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

export default {
    name: 'Profile',
    components: {
        'content-single-column': contentSingleColumn,
        'bread-crumb': breadCrumb,
        'profile-data': profileData,
        'notification-card': notificationCard,
        'password-card': passwordCard
    }
}
</script>
