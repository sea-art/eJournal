<template>
    <content-columns>
        <bread-crumb @eye-click="customisePage" slot="main-content-column" :currentPage="'Settings'"></bread-crumb>

        <profile-card slot="main-content-column"
                      :uname="profile.name"
                      :first="profile.first_name"
                      :last="profile.last_name"
                      :image="profile.picture"
                      :id="profile.uID"
                      :gradeUpdate="profile.grade_notifications"
                      :commentUpdate="profile.comment_notifications">
        </profile-card>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
import profileCard from '@/components/ProfileCard.vue'
import userAPI from '@/api/user.js'

export default {
    name: 'Profile',
    data () {
        return {
            profile: {}
        }
    },
    components: {
        'content-columns': contentColumns,
        'bread-crumb': breadCrumb,
        'profile-card': profileCard
    },
    methods: {
        customisePage () {
            this.$toasted.info('Wishlist: Customise page')
        }
    },
    created () {
        userAPI.getOwnUserData().then(user => { this.profile = user })
    }
}
</script>
