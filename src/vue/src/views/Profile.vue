<template>
    <content-columns>
        <bread-crumb slot="main-content-column" :currentPage="'Settings'"></bread-crumb>

        <profile-card slot="main-content-column" :name="profile[0].name"
                      :email="profile[0].email"
                      :id="profile[0].id">
        </profile-card>
    </content-columns>
</template>

<script>
import contentColumns from '@/components/ContentColumns.vue'
import breadCrumb from '@/components/BreadCrumb.vue'
import profileCard from '@/components/ProfileCard.vue'

export default {
    name: 'Profile',
    data () {
        return {
            profile: [{
                name: 'Engel Hamer',
                email: 'e.hamer@uva.nl',
                id: '11256443',
                image: '../assets/ohno.jpeg'
            }]
        }
    },
    components: {
        'content-columns': contentColumns,
        'bread-crumb': breadCrumb,
        'profile-card': profileCard
    }
}
</script>
