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
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
import profileCard from '@/components/ProfileCard.vue'
import auth from '@/api/auth.js'

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
        auth.get('users/0')
            .then(user => { this.profile = user })
    }
}
</script>
