<template>
    <content-columns>
        <bread-crumb @eye-click="customisePage" slot="main-content-column" :currentPage="'Settings'"></bread-crumb>

        <profile-card slot="main-content-column"
                      :name="profile.name"
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
            alert('Wishlist: Customise page')
        }
    },
    created () {
        userAPI.get_own_user_data().then(user => { this.profile = user })
    }
}
</script>
