<template>
    <b-card class="no-hover">
        <profile-data :uname="uname"
                      :first="first"
                      :last="last"
                      :image="image"
                      :id="id">
        </profile-data>

        <notification-card :gradeUpdate="gradeUpdate"
                           :commentUpdate="commentUpdate"
        ></notification-card>
        <password-card></password-card>
    </b-card>
</template>

<script>
import profileData from '@/components/profile/ProfileData.vue'
import notificationCard from '@/components/profile/NotificationCard.vue'
import passwordCard from '@/components/profile/PasswordCard.vue'

export default {
    props: ['uname', 'first', 'last', 'id', 'image', 'gradeUpdate', 'commentUpdate'],
    components: {
        'profile-data': profileData,
        'notification-card': notificationCard,
        'password-card': passwordCard
    }
}
</script>
