<template>
    <content-columns>
        <profile-card slot="main-content-column"
            :uname="profile.username"
            :first="profile.first_name"
            :last="profile.last_name"
            :image="profile.profile_picture"
            :id="profile.id"
            :gradeUpdate="profile.grade_notifications"
            :commentUpdate="profile.comment_notifications">
        </profile-card>
    </content-single-column>
</template>

<script>
import contentSingleColumn from '@/components/columns/ContentSingleColumn.vue'
import breadCrumb from '@/components/assets/BreadCrumb.vue'
import profileCard from '@/components/profile/ProfileCard.vue'

import auth from '@/api/auth.js'

export default {
    name: 'Profile',
    data () {
        return {
            profile: null
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
        auth.get('users/0')
            .then(user => { this.profile = user })
    }
}
</script>
