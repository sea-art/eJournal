<template>
    <b-card class="settings-card no-hover">
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
import profileData from '@/components/ProfileData.vue'
import notificationCard from '@/components/NotificationCard.vue'
import passwordCard from '@/components/PasswordCard.vue'

export default {
    props: ['uname', 'first', 'last', 'id', 'image', 'gradeUpdate', 'commentUpdate'],
    components: {
        'profile-data': profileData,
        'notification-card': notificationCard,
        'password-card': passwordCard
    }
}
</script>

<style lang="sass">
p.profile-name
    font-size: 30px
    font-weight: bold
    line-height: 35px
    margin-bottom: 0px

p.profile-title
    font-size: 20px
    font-weight: bold
    margin-bottom: 0px

p.profile-data
    font-size: 18px
    line-height: 15px
    margin-bottom: 10px

p.profile-notification
    font-size: 18px
    line-height: 15px
    margin-bottom: 28px

p.profile-password
    font-size: 18px
    line-height: 15px
    margin-bottom: 28px

.profile-col
    padding-left: 0px
</style>
