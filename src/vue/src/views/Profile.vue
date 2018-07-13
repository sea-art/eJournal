<template>
    <content-single-column>
        <bread-crumb @eye-click="customisePage"/>
        <profile-card
            :uname="profile.name"
            :first="profile.first_name"
            :last="profile.last_name"
            :image="profile.picture"
            :id="profile.uID"
            :gradeUpdate="profile.grade_notifications"
            :commentUpdate="profile.comment_notifications">
        </profile-card>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
import profileCard from '@/components/profile/ProfileCard.vue'
import userAPI from '@/api/user.js'

export default {
    name: 'Profile',
    data () {
        return {
            profile: {}
        }
    },
    components: {
        'content-single-column': contentSingleColumn,
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
